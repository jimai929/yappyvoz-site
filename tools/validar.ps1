# Validación antes de publicar: las páginas de descarga coinciden con descargas.json, y cada enlace se puede bajar
# y tiene el tamaño y el SHA-256 que dice la página.
# Uso:  pwsh tools\validar.ps1 && git add -A && git commit ... && git push
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
python -X utf8 tools\generar_descargar.py --comprobar
if ($LASTEXITCODE -ne 0) { Write-Host "VALIDACION: las páginas de descarga no están al día"; exit 1 }
$d = Get-Content descargas.json -Raw -Encoding utf8 | ConvertFrom-Json
$tmp = Join-Path ([IO.Path]::GetTempPath()) "yappyvoz-validar-descargas"
New-Item -ItemType Directory -Force $tmp | Out-Null
foreach ($p in "android", "windows") {
    $x = $d.$p
    $destino = Join-Path $tmp $x.archivo
    curl.exe -sSL --fail -o $destino $x.url
    if ($LASTEXITCODE -ne 0) { Write-Host "VALIDACION: no se puede descargar $($x.url)"; exit 1 }
    $bytes = (Get-Item $destino).Length
    $sha = (Get-FileHash $destino -Algorithm SHA256).Hash
    Write-Host "$($x.archivo)  $bytes bytes  SHA256 $sha"
    if ($bytes -ne $x.bytes -or $sha -ne $x.sha256.ToUpper()) { Write-Host "VALIDACION: $($x.archivo) no coincide con descargas.json"; exit 1 }
    foreach ($pagina in "descargar\index.html", "descargar\zh\index.html", "descargar\en\index.html") {
        $html = Get-Content $pagina -Raw -Encoding utf8
        if (-not $html.Contains($x.url) -or -not $html.Contains($x.sha256.ToLower())) { Write-Host "VALIDACION: $pagina no lleva el enlace o el SHA-256 de $($x.archivo)"; exit 1 }
    }
    Remove-Item $destino
}
if (Select-String -Path descargar\*.html, descargar\*\*.html, activar\*.html -Pattern '<script[^>]+src=|wa\.me/\d' -ErrorAction SilentlyContinue) { Write-Host "VALIDACION: hay un script externo o un número de WhatsApp escrito en una página"; exit 1 }
Write-Host "VALIDACION OK"
exit 0
