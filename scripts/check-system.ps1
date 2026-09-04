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
        [string[]]$Arguments,
        [string[]]$CandidatePaths = @()
    )

    $command = Get-Command $Name
    $executable = if ($null -ne $command) {
        $command.Source
    } else {
        $CandidatePaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    }
    if ($null -eq $executable) {
        return $null
    }

    $result = & $executable @Arguments 2>&1 | Select-Object -First 1
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

$compiler = Get-ChildItem -Path (
    'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\' +
    '*\bin\Hostx64\x64\cl.exe'
) | Sort-Object FullName -Descending | Select-Object -First 1

[ordered]@{
    captured_at = (Get-Date).ToString('o')
    os = [System.Environment]::OSVersion.VersionString
    git = Get-CommandVersion -Name 'git' -Arguments @('--version')
    python = Get-CommandVersion -Name 'python' -Arguments @('--version') -CandidatePaths @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python310\python.exe')
    )
    uv = Get-CommandVersion -Name 'uv' -Arguments @('--version') -CandidatePaths @(
        (Join-Path $PSScriptRoot '..\.venv\Scripts\uv.exe')
    )
    cmake = Get-CommandVersion -Name 'cmake' -Arguments @('--version') -CandidatePaths @(
        'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
    )
    compiler = if ($null -ne $compiler) { $compiler.FullName } else { $null }
    godot = [ordered]@{
        executable = if ($null -ne $godot) { $godot.FullName } else { $null }
        version = $godotVersion
    }
    gpu = $gpu
} | ConvertTo-Json -Depth 4
