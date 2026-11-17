# YappyVoz — sitio

Página informativa y política de privacidad de YappyVoz (GitHub Pages). Sin scripts externos.

- `descargar/` (es, zh, en): se generan con `python tools/generar_descargar.py` a partir de `descargas.json`. Los instaladores
  están en GitHub Releases; aquí solo van el enlace, el tamaño y el SHA-256.
- `activar/`: página puente para el enlace de activación (`/activar/?codigo=…` abre `yappyvoz://activar?codigo=…`).
- Antes de publicar: `pwsh tools\validar.ps1 && git add -A && git commit -m "..." && git push` (baja cada instalador y
  comprueba tamaño y SHA-256).
