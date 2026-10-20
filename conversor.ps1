<#
.SYNOPSIS
    Ejecuta el Conversor de Unidades (mm, cm, m).

.DESCRIPTION
    Cmdlet / script para ejecutar la aplicacion de conversion de unidades.
    Soporta interfaz grafica o ejecucion directa en consola.

.PARAMETER Cli
    Ejecuta el conversor en modo interactivo en la terminal.

.EXAMPLE
    .\conversor.ps1
    Abre la interfaz grafica moderna del conversor.

.EXAMPLE
    .\conversor.ps1 -Cli
    Ejecuta el conversor en modo texto por terminal.
#>

[CmdletBinding()]
param(
    [switch]$Cli
)

$scriptPath = Join-Path $PSScriptRoot "CONVERSOR\app.py"

if (-not (Test-Path $scriptPath)) {
    Write-Error "No se encontro el archivo app.py en '$scriptPath'."
    exit 1
}

if ($Cli) {
    python $scriptPath --cli
} else {
    python $scriptPath
}
