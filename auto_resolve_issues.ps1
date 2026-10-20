<#
.SYNOPSIS
    Worker automatizado con Antigravity CLI (agy) para resolver Issues de GitHub.

.DESCRIPTION
    Revisa periódicamente el repositorio en busca de issues abiertas ('open').
    Para cada issue encontrada:
      1. Genera un prompt con el título, descripción y archivos del proyecto.
      2. Invoca Antigravity CLI (`agy --dangerously-skip-permissions --print "..."`)
         para que analice el código, implemente la solución, haga commit y push.
      3. Lleva un registro de issues procesadas para evitar duplicados.

.PARAMETER IntervalSeconds
    Intervalo de sondeo en segundos (por defecto 30 segundos).

.PARAMETER RunOnce
    Si se especifica, revisa una sola vez y finaliza.
#>

[CmdletBinding()]
param(
    [int]$IntervalSeconds = 30,
    [switch]$RunOnce
)

$RepoOwner = "GonzaloSanchis"
$RepoName = "SPEC-DRIVEN-DEVELOPMENT"
$AgyCmd = "agy.exe"
$ProcessedLogFile = Join-Path $PSScriptRoot ".processed_issues.txt"

if (-not (Test-Path $ProcessedLogFile)) {
    New-Item -ItemType File -Path $ProcessedLogFile -Force | Out-Null
}

function Get-ProcessedIssues {
    if (Test-Path $ProcessedLogFile) {
        return (Get-Content $ProcessedLogFile) | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
    }
    return @()
}

function Mark-IssueProcessed([int]$issueNumber) {
    Add-Content -Path $ProcessedLogFile -Value "$issueNumber"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  ANTIGRAVITY CLI AUTO-RESOLVER DE ISSUES (GITHUB)         " -ForegroundColor Cyan
Write-Host "  Repositorio: $RepoOwner/$RepoName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Modo: $(if ($RunOnce) { 'Ejecucion Unica' } else { "Monitor continuo cada $IntervalSeconds s" })`n"

do {
    try {
        $apiUrl = "https://api.github.com/repos/$RepoOwner/$RepoName/issues?state=open"
        $headers = @{ "User-Agent" = "Antigravity-AutoResolver-PowerShell" }
        $issues = Invoke-RestMethod -Uri $apiUrl -Headers $headers -ErrorAction Stop

        $processed = Get-ProcessedIssues

        # Filtrar solo issues (no Pull Requests) que no hayamos procesado aún
        $pendingIssues = @($issues) | Where-Object { 
            ($null -eq $_.pull_request) -and ($processed -notcontains $_.number)
        }

        if ($pendingIssues.Count -gt 0) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Detectadas $($pendingIssues.Count) issue(s) pendiente(s)!" -ForegroundColor Green

            foreach ($issue in $pendingIssues) {
                $num = $issue.number
                $title = $issue.title
                $author = $issue.user.login
                $body = $issue.body

                Write-Host "`n>>> PROCESANDO ISSUE #$($num): '$title' (por @$author) <<<" -ForegroundColor Yellow

                # Construir la instrucción específica para agy
                $promptText = @"
Tienes la tarea de resolver de forma autonoma la siguiente GitHub Issue del repositorio:
- Issue #$($num): $title
- Autor: @$author
- Descripcion:
$body

INSTRUCCIONES OBLIGATORIAS:
1. Revisa el codigo fuente existente en el directorio de trabajo (especialmente en CONVERSOR/ o la carpeta correspondiente).
2. Modifica el codigo para cumplir y solucionar exactamente lo que pide la issue.
3. Asegurate de que no se rompa la funcionalidad existente.
4. Realiza un commit con git indicando 'Fix #$($num): $title' y sube los cambios inmediatamente a GitHub con 'git push origin main'.
5. Se conciso y directo en tu respuesta final confirmando la solucion.
"@

                Write-Host "Invocando Antigravity CLI (agy)..." -ForegroundColor Magenta

                # Ejecutar agy con auto-aprobación de permisos en el workspace
                & $AgyCmd --dangerously-skip-permissions --print $promptText

                if ($LASTEXITCODE -eq 0) {
                    Write-Host "[✔] Issue #$($num) resuelta y subida a GitHub." -ForegroundColor Green
                    Mark-IssueProcessed -issueNumber $num
                } else {
                    Write-Host "[!] agy finalizó con código de salida $LASTEXITCODE para la issue #$($num)." -ForegroundColor Red
                }
            }
        } else {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sin issues pendientes. Monitorizando..." -ForegroundColor Gray
        }
    } catch {
        Write-Host "[!] Error al consultar GitHub: $($_.Exception.Message)" -ForegroundColor Red
    }

    if (-not $RunOnce) {
        Start-Sleep -Seconds $IntervalSeconds
    }
} while (-not $RunOnce)
