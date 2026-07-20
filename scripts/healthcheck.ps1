[CmdletBinding()]
param(
    [string]$EnvFile = $env:HOSPRIME_ENV_FILE,
    [string]$ProjectName = $env:HOSPRIME_COMPOSE_PROJECT_NAME,
    [string]$ExpectedGitSha = $env:HOSPRIME_EXPECTED_GIT_SHA
)

$ErrorActionPreference = 'Stop'
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($EnvFile)) { $EnvFile = Join-Path $RootDir '.env' }
if (-not [System.IO.Path]::IsPathRooted($EnvFile)) { $EnvFile = Join-Path (Get-Location).Path $EnvFile }
$EnvFile = [System.IO.Path]::GetFullPath($EnvFile)
if ([string]::IsNullOrWhiteSpace($ProjectName)) { $ProjectName = 'hosprime' }

function Fail([string]$Message) { throw $Message }
function Assert-RegularEnvFile([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.PSIsContainer) { Fail "Environment path is not a regular file: $Path" }
    if ($item.LinkType) { Fail "Environment file must not be a symbolic link: $Path" }
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
    if ($status.Count -ne 0) { Fail 'HosPrime checkout must be pristine for health evidence.' }
}
function Assert-Port([string]$Key, [string]$Value) {
    $port = 0
    if (-not [int]::TryParse($Value, [ref]$port) -or $port -lt 1 -or $port -gt 65535) { Fail "$Key must be an integer between 1 and 65535." }
}
function Get-PublishedPort([string]$Service, [int]$ContainerPort) {
    $bindings = @(& docker compose --project-name $ProjectName --env-file $EnvFile port $Service $ContainerPort | ForEach-Object { $_.Trim() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { Fail "Unable to resolve published port for ${Service}:$ContainerPort." }
    if ($bindings.Count -eq 0) { Fail "No published host port for ${Service}:$ContainerPort in Compose project $ProjectName." }
    if ($bindings.Count -ne 1) { Fail "Expected one published host port for ${Service}:$ContainerPort in Compose project $ProjectName." }
    $match = [regex]::Match($bindings[0], '^127\.0\.0\.1:(\d+)$')
    if (-not $match.Success) {
        if ($bindings[0] -notmatch ':\d+$') { Fail "Unexpected published-port binding for ${Service}:$ContainerPort." }
        Fail "Published binding must use 127.0.0.1 for ${Service}:$ContainerPort in Compose project $ProjectName."
    }
    $port = $match.Groups[1].Value
    Assert-Port "${Service}_PUBLISHED_PORT" $port
    return $port
}
function Get-ServiceContainerId([string]$Service) {
    $ids = @(& docker compose --project-name $ProjectName --env-file $EnvFile ps -q $Service | ForEach-Object { $_.Trim() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
    if ($LASTEXITCODE -ne 0) { Fail "Unable to inspect service: $Service" }
    if ($ids.Count -eq 0) { Fail "Service container does not exist in Compose project ${ProjectName}: $Service" }
    if ($ids.Count -ne 1) { Fail "Expected exactly one container for service $Service in Compose project $ProjectName" }
    if ($ids[0] -notmatch '^[0-9a-f]{12,64}$') { Fail "Unexpected container identifier for service $Service" }
    return $ids[0]
}
function Get-ContainerState([string]$ContainerId) { $v=[string]::Join('',@(& docker inspect --format '{{.State.Status}}' $ContainerId)).Trim(); if($LASTEXITCODE-ne 0){Fail "Unable to inspect container state: $ContainerId"}; return $v }
function Get-ContainerHealth([string]$ContainerId) { $v=[string]::Join('',@(& docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $ContainerId)).Trim(); if($LASTEXITCODE-ne 0){Fail "Unable to inspect container health: $ContainerId"}; return $v }
function Get-ContainerComposeIdentity([string]$ContainerId) { $v=[string]::Join('',@(& docker inspect --format '{{ index .Config.Labels "com.docker.compose.project" }}|{{ index .Config.Labels "com.docker.compose.service" }}' $ContainerId)).Trim(); if($LASTEXITCODE-ne 0){Fail "Unable to inspect Compose identity: $ContainerId"}; return $v }
function Get-ContainerImageId([string]$ContainerId) { $v=[string]::Join('',@(& docker inspect --format '{{.Image}}' $ContainerId)).Trim(); if($LASTEXITCODE-ne 0 -or $v -notmatch '^sha256:[0-9a-f]{64}$'){Fail "Unable to resolve a valid image identity for container $ContainerId"}; return $v }
function Get-ImageSourceRevision([string]$ImageId) { $v=[string]::Join('',@(& docker image inspect --format '{{ index .Config.Labels "org.opencontainers.image.revision" }}' $ImageId)).Trim(); if($LASTEXITCODE-ne 0 -or $v -notmatch '^[0-9a-f]{40}$'){Fail "Application image is missing a valid source revision label"}; return $v }

if ($ProjectName -notmatch '^[a-z0-9][a-z0-9_-]*$') { Fail 'ProjectName must match ^[a-z0-9][a-z0-9_-]*$.' }
if (-not [string]::IsNullOrWhiteSpace($ExpectedGitSha) -and $ExpectedGitSha -notmatch '^[0-9a-f]{40}$') { Fail 'ExpectedGitSha must be a full lowercase commit SHA.' }
if (-not (Test-Path -LiteralPath $EnvFile -PathType Leaf)) { Fail "Environment path is not a regular file: $EnvFile" }
Assert-RegularEnvFile $EnvFile
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'Docker is required.' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail 'Git is required.' }
& docker compose version *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose v2 is required.' }

$PreviousBuildGitSha = $env:HOSPRIME_BUILD_GIT_SHA
Push-Location $RootDir
try {
    $SourceSha = Get-ExactSourceSha
    Assert-PristineCheckout
    if (-not [string]::IsNullOrWhiteSpace($ExpectedGitSha) -and $SourceSha -ne $ExpectedGitSha) { Fail 'HosPrime source commit changed between bootstrap and health verification.' }
    $env:HOSPRIME_BUILD_GIT_SHA = $SourceSha
    $status = Invoke-Compose config --quiet
    if ($status -ne 0) { Fail 'Docker Compose configuration validation failed.' }
    foreach ($service in @('postgres', 'redis', 'neo4j', 'backend', 'frontend')) {
        $containerId = Get-ServiceContainerId $service
        $identity = Get-ContainerComposeIdentity $containerId
        if ($identity -ne "${ProjectName}|${service}") { Fail "Container identity mismatch for service $service in Compose project $ProjectName" }
        $state = Get-ContainerState $containerId
        if ($state -ne 'running') { Fail "Service is not running: $service ($state)" }
        $health = Get-ContainerHealth $containerId
        if ($health -ne 'healthy') { Fail "Service is not healthy: $service ($health)" }
        if ($service -in @('backend', 'frontend')) {
            $imageId = Get-ContainerImageId $containerId
            $revision = Get-ImageSourceRevision $imageId
            if ($revision -ne $SourceSha) { Fail "Application image source revision mismatch for service $service" }
        }
    }
    $PostgresPort = Get-PublishedPort 'postgres' 5432
    $RedisPort = Get-PublishedPort 'redis' 6379
    $Neo4jHttpPort = Get-PublishedPort 'neo4j' 7474
    $Neo4jBoltPort = Get-PublishedPort 'neo4j' 7687
    $BackendPort = Get-PublishedPort 'backend' 8000
    $FrontendPort = Get-PublishedPort 'frontend' 80
    $BackendUrl = "http://127.0.0.1:$BackendPort"
    $FrontendUrl = "http://127.0.0.1:$FrontendPort"
    $live = Invoke-RestMethod -Uri "$BackendUrl/health/live" -TimeoutSec 15
    $ready = Invoke-RestMethod -Uri "$BackendUrl/health/ready" -TimeoutSec 15
    $frontend = Invoke-WebRequest -Uri "$FrontendUrl/" -TimeoutSec 15 -UseBasicParsing
    if ($live.status -ne 'live') { Fail 'Backend liveness contract failed.' }
    if ($ready.status -ne 'ready') { Fail 'Backend readiness contract failed.' }
    if ($ready.database_dialect -ne 'postgresql') { Fail 'Backend database readiness contract failed.' }
    if (@($ready.configuration_warnings).Count -ne 0) { Fail 'Backend reported security or configuration warnings.' }
    $expectedCapabilityWarnings = @('External AI provider is not configured')
    $actualCapabilityWarnings = @($ready.capability_warnings)
    if ($actualCapabilityWarnings.Count -ne $expectedCapabilityWarnings.Count -or
        [string]::Join("`n", $actualCapabilityWarnings) -cne [string]::Join("`n", $expectedCapabilityWarnings)) {
        Fail 'Backend provider capability evidence is incomplete or unexpected.'
    }
    if ([string]::IsNullOrWhiteSpace($frontend.Content)) { Fail 'Frontend returned an empty response.' }
    Write-Host "HosPrime health check passed (Compose project: $ProjectName, source commit: $SourceSha)."
    Write-Host "Verified loopback bindings: postgres=$PostgresPort redis=$RedisPort neo4j-http=$Neo4jHttpPort neo4j-bolt=$Neo4jBoltPort backend=$BackendPort frontend=$FrontendPort"
    Write-Host "Backend: $BackendUrl"
    Write-Host "Frontend: $FrontendUrl"
    $status = Invoke-Compose ps
    if ($status -ne 0) { Fail 'Unable to record Compose service state.' }
}
finally {
    $env:HOSPRIME_BUILD_GIT_SHA = $PreviousBuildGitSha
    Pop-Location
}
