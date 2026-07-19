[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [string]$EnvFile = $env:HOSPRIME_ENV_FILE,
    [string]$ProjectName = $env:HOSPRIME_COMPOSE_PROJECT_NAME
)

$ErrorActionPreference = 'Stop'
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($EnvFile)) { $EnvFile = Join-Path $RootDir '.env' }
if (-not [System.IO.Path]::IsPathRooted($EnvFile)) {
    $EnvFile = Join-Path (Get-Location).Path $EnvFile
}
$EnvFile = [System.IO.Path]::GetFullPath($EnvFile)
if ([string]::IsNullOrWhiteSpace($ProjectName)) { $ProjectName = 'hosprime' }

function Fail([string]$Message) { throw $Message }
function Assert-RegularEnvFile([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.PSIsContainer) { Fail "Environment path is not a regular file: $Path" }
    if ($item.LinkType) { Fail "Environment file must not be a symbolic link: $Path" }
}
function Assert-InRepoEnvIsIgnored([string]$Path) {
    $rootPrefix = $RootDir.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if ($Path.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relativePath = $Path.Substring($rootPrefix.Length).Replace('\', '/')
        & git check-ignore -q -- $relativePath
        if ($LASTEXITCODE -ne 0) { Fail "Environment file inside repository must be ignored by Git: $relativePath" }
    }
}
function Invoke-Compose([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments) {
    & docker compose --project-name $ProjectName --env-file $EnvFile @Arguments
    return $LASTEXITCODE
}
function Get-ExactSourceSha() {
    $sha = [string]::Join('', @(& git rev-parse --verify HEAD 2>$null)).Trim()
    if ($LASTEXITCODE -ne 0 -or $sha -notmatch '^[0-9a-f]{40}$') { Fail 'Unable to resolve an exact HosPrime source commit.' }
    return $sha
}
function Assert-PristineCheckout() {
    $status = @(& git status --porcelain=v1 --untracked-files=all)
    if ($LASTEXITCODE -ne 0) { Fail 'Unable to inspect HosPrime checkout status.' }
    if ($status.Count -ne 0) { Fail 'HosPrime checkout must be pristine before bootstrap.' }
}

if ($ProjectName -notmatch '^[a-z0-9][a-z0-9_-]*$') { Fail 'ProjectName must match ^[a-z0-9][a-z0-9_-]*$.' }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'Docker is required.' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail 'Git is required.' }
& docker info *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker daemon is not available.' }
& docker compose version *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose v2 is required.' }

$PreviousBuildGitSha = $env:HOSPRIME_BUILD_GIT_SHA
Push-Location $RootDir
try {
    $SourceSha = Get-ExactSourceSha
    Assert-PristineCheckout
    $env:HOSPRIME_BUILD_GIT_SHA = $SourceSha

    if (-not (Test-Path -LiteralPath $EnvFile)) {
        $parent = Split-Path -Parent $EnvFile
        if (-not (Test-Path -LiteralPath $parent -PathType Container)) { Fail "Environment file parent directory does not exist: $parent" }
        Copy-Item -LiteralPath (Join-Path $RootDir '.env.example') -Destination $EnvFile
        Write-Host "Created $EnvFile from .env.example. Replace every CHANGE_ME value, then run this command again."
        exit 2
    }
    Assert-RegularEnvFile $EnvFile
    Assert-InRepoEnvIsIgnored $EnvFile

    $placeholderLine = Get-Content -LiteralPath $EnvFile | Where-Object {
        $_ -notmatch '^\s*(#|$)' -and $_ -match 'CHANGE_ME'
    } | Select-Object -First 1
    if ($null -ne $placeholderLine) {
        Fail "$EnvFile still contains CHANGE_ME placeholders."
    }

    $status = Invoke-Compose config --quiet
    if ($status -ne 0) { Fail 'Docker Compose configuration validation failed.' }

    if (-not $SkipBuild) {
        $status = Invoke-Compose build
        if ($status -ne 0) { Fail 'Docker image build failed.' }
    }

    $status = Invoke-Compose up --detach --wait --wait-timeout 240
    if ($status -ne 0) { Fail 'HosPrime stack did not become healthy.' }

    & (Join-Path $PSScriptRoot 'healthcheck.ps1') -EnvFile $EnvFile -ProjectName $ProjectName -ExpectedGitSha $SourceSha
    if ($LASTEXITCODE -ne 0) { Fail 'HosPrime health check failed.' }
    Write-Host "HosPrime local stack is ready (Compose project: $ProjectName, source commit: $SourceSha)."
}
finally {
    $env:HOSPRIME_BUILD_GIT_SHA = $PreviousBuildGitSha
    Pop-Location
}
