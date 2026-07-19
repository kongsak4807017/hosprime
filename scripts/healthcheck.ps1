[CmdletBinding()]
param(
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
function Invoke-Compose([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments) {
    & docker compose --project-name $ProjectName --env-file $EnvFile @Arguments
    return $LASTEXITCODE
}
function Assert-Port([string]$Key, [string]$Value) {
    $port = 0
    if (-not [int]::TryParse($Value, [ref]$port) -or $port -lt 1 -or $port -gt 65535) {
        Fail "$Key must be an integer between 1 and 65535."
    }
}
function Get-PublishedPort([string]$Service, [int]$ContainerPort) {
    $bindings = @(& docker compose --project-name $ProjectName --env-file $EnvFile port $Service $ContainerPort)
    if ($LASTEXITCODE -ne 0) { Fail "Unable to resolve published port for ${Service}:$ContainerPort." }

    $ports = @(
        $bindings |
            ForEach-Object {
                $match = [regex]::Match($_.Trim(), ':(\d+)$')
                if (-not $match.Success) { Fail "Unexpected published-port binding for ${Service}:$ContainerPort." }
                $match.Groups[1].Value
            } |
            Sort-Object -Unique
    )
    if ($ports.Count -ne 1) {
        Fail "Expected one published host port for ${Service}:$ContainerPort in Compose project $ProjectName."
    }
    Assert-Port "${Service}_PUBLISHED_PORT" $ports[0]
    return $ports[0]
}
function Get-ServiceContainerId([string]$Service) {
    $id = [string]::Join('', @(& docker compose --project-name $ProjectName --env-file $EnvFile ps -q $Service)).Trim()
    if ($LASTEXITCODE -ne 0) { Fail "Unable to inspect service: $Service" }
    if ([string]::IsNullOrWhiteSpace($id)) { Fail "Service container does not exist in Compose project $ProjectName: $Service" }
    return $id
}
function Get-ContainerState([string]$ContainerId) {
    $state = [string]::Join('', @(& docker inspect --format '{{.State.Status}}' $ContainerId)).Trim()
    if ($LASTEXITCODE -ne 0) { Fail "Unable to inspect container state: $ContainerId" }
    return $state
}
function Get-ContainerHealth([string]$ContainerId) {
    $health = [string]::Join('', @(& docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $ContainerId)).Trim()
    if ($LASTEXITCODE -ne 0) { Fail "Unable to inspect container health: $ContainerId" }
    return $health
}

if ($ProjectName -notmatch '^[a-z0-9][a-z0-9_-]*$') { Fail 'ProjectName must match ^[a-z0-9][a-z0-9_-]*$.' }
if (-not (Test-Path -LiteralPath $EnvFile -PathType Leaf)) { Fail "Environment path is not a regular file: $EnvFile" }
Assert-RegularEnvFile $EnvFile
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'Docker is required.' }
& docker compose version *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose v2 is required.' }

Push-Location $RootDir
try {
    $status = Invoke-Compose config --quiet
    if ($status -ne 0) { Fail 'Docker Compose configuration validation failed.' }

    foreach ($service in @('postgres', 'redis', 'neo4j', 'backend', 'frontend')) {
        $containerId = Get-ServiceContainerId $service
        $state = Get-ContainerState $containerId
        if ($state -ne 'running') { Fail "Service is not running: $service ($state)" }
        $health = Get-ContainerHealth $containerId
        if ($health -ne 'healthy') { Fail "Service is not healthy: $service ($health)" }
    }

    $BackendPort = Get-PublishedPort 'backend' 8000
    $FrontendPort = Get-PublishedPort 'frontend' 80
    $BackendUrl = "http://127.0.0.1:$BackendPort"
    $FrontendUrl = "http://127.0.0.1:$FrontendPort"

    $live = Invoke-RestMethod -Uri "$BackendUrl/health/live" -TimeoutSec 15
    $ready = Invoke-RestMethod -Uri "$BackendUrl/health/ready" -TimeoutSec 15
    $frontend = Invoke-WebRequest -Uri "$FrontendUrl/" -TimeoutSec 15 -UseBasicParsing

    if ($live.status -ne 'live') { Fail "Unexpected liveness status: $($live.status)" }
    if ($ready.status -ne 'ready') { Fail "Backend is not fully ready: $($ready.status)" }
    if ($ready.database_dialect -ne 'postgresql') { Fail "Expected PostgreSQL runtime; got $($ready.database_dialect)" }
    if ([string]::IsNullOrWhiteSpace($frontend.Content)) { Fail 'Frontend returned an empty response.' }

    Write-Host "HosPrime health check passed (Compose project: $ProjectName)."
    Write-Host "Backend: $BackendUrl"
    Write-Host "Frontend: $FrontendUrl"
    $status = Invoke-Compose ps
    if ($status -ne 0) { Fail 'Unable to record Compose service state.' }
}
finally {
    Pop-Location
}
