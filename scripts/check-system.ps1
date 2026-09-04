[CmdletBinding()]
param(
    [string]$GodotDirectory = 'C:\Godot-472'
)

$ErrorActionPreference = 'SilentlyContinue'

function Get-CommandVersion {
    param(
        [Parameter(Mandatory)]
        [string]$Name,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    $command = Get-Command $Name
    if ($null -eq $command) {
        return $null
    }

    $result = & $command.Source @Arguments 2>&1 | Select-Object -First 1
    return [string]$result
}

$godot = Get-ChildItem -LiteralPath $GodotDirectory -Filter '*_console.exe' |
    Select-Object -First 1
$godotVersion = $null
if ($null -ne $godot) {
    $godotVersion = [string](& $godot.FullName --version 2>&1 | Select-Object -First 1)
}

$gpu = $null
if ($null -ne (Get-Command nvidia-smi)) {
    $gpuLine = & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>&1 |
        Select-Object -First 1
    if ($gpuLine -is [string]) {
        $parts = $gpuLine -split ',\s*'
        if ($parts.Count -ge 3) {
            $gpu = [ordered]@{
                name = $parts[0]
                memory_total = $parts[1]
                driver_version = $parts[2]
            }
        }
    }
}

[ordered]@{
    captured_at = (Get-Date).ToString('o')
    os = [System.Environment]::OSVersion.VersionString
    git = Get-CommandVersion -Name 'git' -Arguments @('--version')
    python = Get-CommandVersion -Name 'python' -Arguments @('--version')
    uv = Get-CommandVersion -Name 'uv' -Arguments @('--version')
    cmake = Get-CommandVersion -Name 'cmake' -Arguments @('--version')
    compiler = if ($null -ne (Get-Command cl.exe)) { (Get-Command cl.exe).Source } else { $null }
    godot = [ordered]@{
        executable = if ($null -ne $godot) { $godot.FullName } else { $null }
        version = $godotVersion
    }
    gpu = $gpu
} | ConvertTo-Json -Depth 4
