# Build and publish ms-dos.su.
#
#   .\deploy.ps1                 # build + checks only
#   .\deploy.ps1 -Push           # build, commit and push docs/
#   .\deploy.ps1 -Push -Message "site: update demo"
#
# Requires: python 3.11+ on PATH (or set $env:MBFU_PYTHON), git, and a
# repository whose /docs folder is the GitHub Pages source.
param(
    [switch]$Push,
    [string]$Message = "site: rebuild ms-dos.su",
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = if ($env:MBFU_PYTHON) { $env:MBFU_PYTHON } else { "python" }

Push-Location $root
try {
    # 1. Fresh demo archive, if a build exists next to the repo.
    $demo = Join-Path $root "..\mbfu-work\demo\out\MBFUTool_2.0_Demo_Portable.zip"
    if (Test-Path $demo) {
        New-Item -ItemType Directory -Force -Path (Join-Path $root "docs\downloads") | Out-Null
        Copy-Item $demo (Join-Path $root "docs\downloads") -Force
        Write-Host "demo archive copied"
    } else {
        Write-Warning "demo archive not found, publishing the existing one"
    }

    # 2. Regenerate every page.
    Push-Location (Join-Path $root "tools")
    try {
        & $py gen_site.py
        if ($LASTEXITCODE -ne 0) { throw "gen_site.py failed" }
        & $py gen_seo.py
        if ($LASTEXITCODE -ne 0) { throw "gen_seo.py failed" }
        & $py gen_sitemap.py
        if ($LASTEXITCODE -ne 0) { throw "gen_sitemap.py failed" }
    } finally {
        Pop-Location
    }

    # 3. Link / JSON-LD / token check. Refuses to publish a broken tree.
    Push-Location (Join-Path $root "tools")
    try {
        & $py check_site.py
        if ($LASTEXITCODE -ne 0) { throw "check_site.py found problems" }
    } finally {
        Pop-Location
    }

    if (-not $Push) {
        Write-Host "build OK (not pushed)"
        return
    }

    # 4. Commit and push.
    git add docs
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        git commit -m $Message
        if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
    } else {
        Write-Host "nothing to commit"
    }

    # TLS in sandboxed shells may fail with schannel errors; OpenSSL backend
    # is a working fallback in that case.
    git push $Remote $Branch
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "push failed, retrying with the OpenSSL backend"
        git -c http.sslBackend=openssl push $Remote $Branch
        if ($LASTEXITCODE -ne 0) { throw "push failed" }
    }
    Write-Host "published to $Remote/$Branch"
} finally {
    Pop-Location
}