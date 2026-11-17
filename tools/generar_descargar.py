"""
Genera descargar/index.html (es), descargar/zh/ y descargar/en/ a partir de descargas.json.
Los instaladores están en GitHub Releases; las páginas solo llevan el enlace, el tamaño y el SHA-256.

  python tools/generar_descargar.py            escribe las tres páginas
  python tools/generar_descargar.py --comprobar  no escribe: falla si alguna página no coincide con descargas.json

Sin scripts ni recursos externos. Si existe descargar/qr.svg (código QR de la página), se enseña.
"""
import html
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://voz.gestorpro.us"
RUTAS = {"es": "descargar/index.html", "zh": "descargar/zh/index.html", "en": "descargar/en/index.html"}
NOMBRES = {"es": "Español", "zh": "中文", "en": "English"}

T = {
    "es": {
        "titulo": "Descargar YappyVoz", "desc": "Descarga e instalación de YappyVoz para Android y Windows, paso a paso.",
        "sub": "Instálelo usted mismo en unos minutos. Al abrirlo, una guía le lleva paso a paso.",
        "qr": "Para abrir esta página en el teléfono, apunte la cámara a este código.",
        "android": "Android (teléfono)", "windows": "Windows (computadora)",
        "bajar_apk": "Descargar para Android", "bajar_exe": "Descargar para Windows",
        "version": "Versión", "tamano": "Tamaño", "sha": "SHA-256",
        "a1": "Toque <strong>Descargar para Android</strong>. Si el navegador avisa de que el archivo puede ser dañino, elija <strong>Descargar de todos modos</strong>.",
        "a2": "Abra el archivo descargado (aparece abajo en el navegador o en la carpeta <em>Descargas</em>).",
        "a3": "El teléfono preguntará si permite instalar aplicaciones desde el navegador. Elija su marca:",
        "a4": "Toque <strong>Instalar</strong>. Si Play Protect pregunta, elija <strong>Instalar de todas formas</strong>.",
        "a5": "Abra <strong>YappyVoz Gmail</strong> y siga la guía: cada pantalla tiene un botón que abre el ajuste que hay que cambiar.",
        "marcas": {
            "Honor / Huawei": ["Aparece «Por su seguridad, el teléfono no permite instalar aplicaciones de esta fuente». Toque <strong>Ajustes</strong>.",
                               "Encienda <strong>Permitir la instalación de aplicaciones</strong> y vuelva atrás.",
                               "Si aparece «Instalación de aplicaciones externas», marque que entiende el riesgo y toque <strong>Continuar</strong>."],
            "Samsung": ["Toque <strong>Ajustes</strong> en el aviso y encienda <strong>Permitir de esta fuente</strong>.",
                        "Si dice que el <em>Bloqueo automático</em> lo impide: Ajustes → Seguridad y privacidad → Bloqueo automático → apagar, e intente de nuevo."],
            "Xiaomi / Redmi / POCO": ["Toque <strong>Ajustes</strong> en el aviso y encienda <strong>Permitir de esta fuente</strong>.",
                                      "MIUI muestra una advertencia con cuenta atrás de 10 segundos: espere y toque <strong>Aceptar</strong>."],
            "Motorola": ["Toque <strong>Configuración</strong> en el aviso y encienda <strong>Permitir desde esta fuente</strong>; vuelva atrás."],
            "Otros": ["Toque <strong>Ajustes</strong> en el aviso y encienda <strong>Permitir de esta fuente</strong> (o «Instalar aplicaciones desconocidas»); vuelva atrás."],
        },
        "w1": "Haga clic en <strong>Descargar para Windows</strong> y abra <code>{exe}</code>.",
        "w2": "Windows muestra una ventana azul, «Windows protegió su PC», porque el programa es nuevo. Haga clic en <strong>Más información</strong> y después en <strong>Ejecutar de todas formas</strong>.",
        "w3": "Siga el instalador (no pide contraseña de administrador). Al terminar se abre solo el asistente de YappyVoz.",
        "ss_titulo": "Windows protegió su PC", "ss_texto": "SmartScreen de Microsoft Defender impidió el inicio de una aplicación desconocida.",
        "ss_mas": "Más información", "ss_ejecutar": "Ejecutar de todas formas", "ss_no": "No ejecutar", "paso": "Paso",
        "activar": "Activación", "activar_texto": "En la guía, toque <strong>Enviar por WhatsApp</strong>: nos llega el código de su equipo y le devolvemos un enlace. Al tocar el enlace, YappyVoz queda activado.",
        "comprobar": "Comprobar la descarga (opcional)", "comprobar_texto": "En Windows, abra PowerShell y escriba <code>Get-FileHash archivo</code>: el resultado debe ser igual al SHA-256 de arriba.",
        "aviso": "YappyVoz es un desarrollo independiente. <strong>No está afiliado a Yappy ni a Banco General.</strong>",
        "inicio": "Inicio", "privacidad": "Política de privacidad",
    },
    "zh": {
        "titulo": "下载 YappyVoz", "desc": "YappyVoz 安卓版和 Windows 版的下载与安装步骤。",
        "sub": "几分钟就能自己装好。打开后有向导一步一步带着做。",
        "qr": "想在手机上打开本页，用相机扫这个码。",
        "android": "安卓（手机）", "windows": "Windows（电脑）",
        "bajar_apk": "下载安卓版", "bajar_exe": "下载 Windows 版",
        "version": "版本", "tamano": "大小", "sha": "SHA-256",
        "a1": "点<strong>下载安卓版</strong>。浏览器如果提示文件可能有害，选<strong>仍然下载</strong>。",
        "a2": "打开下载好的文件（浏览器底部，或“下载”文件夹里）。",
        "a3": "手机会问是否允许从浏览器安装应用。按你的手机品牌操作：",
        "a4": "点<strong>安装</strong>。如果 Play Protect 询问，选<strong>仍然安装</strong>。",
        "a5": "打开 <strong>YappyVoz Gmail</strong>，跟着向导做：每一屏都有按钮，直接跳到要改的设置。",
        "marcas": {
            "荣耀 / 华为": ["出现“为了安全，手机不允许安装此来源的应用”，点<strong>设置</strong>。",
                          "打开<strong>允许安装应用</strong>，然后返回。",
                          "如果出现“外部来源应用安装”，勾选已了解风险，点<strong>继续安装</strong>。"],
            "三星": ["在提示里点<strong>设置</strong>，打开<strong>允许来自此来源</strong>。",
                     "如果提示被“自动拦截”阻止：设置 → 安全和隐私 → 自动拦截 → 关闭，再试一次。"],
            "小米 / Redmi / POCO": ["在提示里点<strong>设置</strong>，打开<strong>允许来自此来源</strong>。",
                                    "MIUI 会显示 10 秒倒计时的警告：等它结束，点<strong>确定</strong>。"],
            "摩托罗拉": ["在提示里点<strong>设置</strong>，打开<strong>允许来自此来源</strong>，然后返回。"],
            "其他": ["在提示里点<strong>设置</strong>，打开<strong>允许来自此来源</strong>（或“安装未知应用”），然后返回。"],
        },
        "w1": "点<strong>下载 Windows 版</strong>，打开 <code>{exe}</code>。",
        "w2": "因为程序是新的，Windows 会弹出蓝色窗口“Windows 已保护你的电脑”。点<strong>更多信息</strong>，再点<strong>仍要运行</strong>。",
        "w3": "按安装程序走完（不需要管理员密码）。装完后 YappyVoz 的向导会自动打开。",
        "ss_titulo": "Windows 已保护你的电脑", "ss_texto": "Microsoft Defender SmartScreen 阻止了一个未识别的应用启动。",
        "ss_mas": "更多信息", "ss_ejecutar": "仍要运行", "ss_no": "不运行", "paso": "第",
        "activar": "激活", "activar_texto": "在向导里点<strong>用 WhatsApp 发送</strong>：我们收到你的设备码后回一个链接，点一下链接就激活了。",
        "comprobar": "核对下载的文件（可选）", "comprobar_texto": "在 Windows 打开 PowerShell，输入 <code>Get-FileHash 文件名</code>：结果应与上面的 SHA-256 相同。",
        "aviso": "YappyVoz 是独立开发的工具，<strong>与 Yappy 和 Banco General 没有关联。</strong>",
        "inicio": "首页", "privacidad": "隐私政策",
    },
    "en": {
        "titulo": "Download YappyVoz", "desc": "How to download and install YappyVoz for Android and Windows, step by step.",
        "sub": "Install it yourself in a few minutes. When you open it, a guide walks you through each step.",
        "qr": "To open this page on your phone, point the camera at this code.",
        "android": "Android (phone)", "windows": "Windows (computer)",
        "bajar_apk": "Download for Android", "bajar_exe": "Download for Windows",
        "version": "Version", "tamano": "Size", "sha": "SHA-256",
        "a1": "Tap <strong>Download for Android</strong>. If the browser warns the file may be harmful, choose <strong>Download anyway</strong>.",
        "a2": "Open the downloaded file (at the bottom of the browser, or in the <em>Downloads</em> folder).",
        "a3": "The phone asks whether to allow installing apps from the browser. Pick your brand:",
        "a4": "Tap <strong>Install</strong>. If Play Protect asks, choose <strong>Install anyway</strong>.",
        "a5": "Open <strong>YappyVoz Gmail</strong> and follow the guide: every screen has a button that opens the setting to change.",
        "marcas": {
            "Honor / Huawei": ["“For your security, your phone is not allowed to install apps from this source” appears. Tap <strong>Settings</strong>.",
                               "Turn on <strong>Allow app installs</strong> and go back.",
                               "If “External app installation” appears, tick that you understand the risk and tap <strong>Continue</strong>."],
            "Samsung": ["Tap <strong>Settings</strong> in the notice and turn on <strong>Allow from this source</strong>.",
                        "If <em>Auto Blocker</em> stops it: Settings → Security and privacy → Auto Blocker → off, then try again."],
            "Xiaomi / Redmi / POCO": ["Tap <strong>Settings</strong> in the notice and turn on <strong>Allow from this source</strong>.",
                                      "MIUI shows a warning with a 10-second countdown: wait and tap <strong>OK</strong>."],
            "Motorola": ["Tap <strong>Settings</strong> in the notice and turn on <strong>Allow from this source</strong>; go back."],
            "Others": ["Tap <strong>Settings</strong> in the notice and turn on <strong>Allow from this source</strong> (or “Install unknown apps”); go back."],
        },
        "w1": "Click <strong>Download for Windows</strong> and open <code>{exe}</code>.",
        "w2": "Windows shows a blue window, “Windows protected your PC”, because the program is new. Click <strong>More info</strong> and then <strong>Run anyway</strong>.",
        "w3": "Follow the installer (no administrator password needed). When it finishes, the YappyVoz wizard opens by itself.",
        "ss_titulo": "Windows protected your PC", "ss_texto": "Microsoft Defender SmartScreen prevented an unrecognized app from starting.",
        "ss_mas": "More info", "ss_ejecutar": "Run anyway", "ss_no": "Don't run", "paso": "Step",
        "activar": "Activation", "activar_texto": "In the guide, tap <strong>Send by WhatsApp</strong>: we receive your device code and send back a link. Tap the link and YappyVoz is activated.",
        "comprobar": "Check the download (optional)", "comprobar_texto": "On Windows, open PowerShell and type <code>Get-FileHash file</code>: the result must equal the SHA-256 above.",
        "aviso": "YappyVoz is an independent project. <strong>It is not affiliated with Yappy or Banco General.</strong>",
        "inicio": "Home", "privacidad": "Privacy policy",
    },
}

CSS = """
    :root { color-scheme: light; }
    body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Microsoft YaHei", "PingFang SC", sans-serif; color: #1c1c1c; background: #fafafa; line-height: 1.6; }
    main { max-width: 760px; margin: 0 auto; padding: 32px 20px 56px; }
    h1 { font-size: 2rem; margin: 0 0 8px; }
    h2 { font-size: 1.35rem; margin: 40px 0 8px; }
    .idiomas { margin: 0 0 20px; font-size: 0.95rem; }
    .sub { color: #555; font-size: 1.1rem; margin: 0 0 24px; }
    .boton { display: inline-block; background: #1f7a5c; color: #fff; text-decoration: none; font-weight: 700; font-size: 1.15rem; padding: 14px 28px; border-radius: 28px; margin: 8px 0; }
    .datos { color: #555; font-size: 0.9rem; margin: 4px 0 16px; }
    .datos code { word-break: break-all; }
    ol { padding-left: 22px; } ol > li { margin: 10px 0; }
    details { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 8px 14px; margin: 8px 0; }
    summary { font-weight: 700; cursor: pointer; }
    .qr { display: flex; gap: 16px; align-items: center; background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 12px 16px; margin: 16px 0; }
    .qr img { width: 132px; height: 132px; }
    .pantallas { display: flex; flex-wrap: wrap; gap: 14px; margin: 12px 0; }
    .ss { background: #0067c0; color: #fff; width: 300px; padding: 16px 18px; border-radius: 4px; font-family: "Segoe UI", system-ui, sans-serif; font-size: 0.85rem; }
    .ss b { display: block; font-size: 1.1rem; font-weight: 600; margin: 4px 0 8px; }
    .ss small { display: block; opacity: 0.8; margin-bottom: 6px; }
    .ss u { display: inline-block; margin-top: 6px; }
    .ss .fila { text-align: right; margin-top: 18px; }
    .ss span { display: inline-block; border: 2px solid #fff; padding: 4px 12px; margin-left: 6px; }
    .ss .marca { outline: 3px solid #ffd54a; outline-offset: 3px; }
    .aviso { background: #fff4e5; border-left: 4px solid #e6a23c; padding: 12px 16px; border-radius: 4px; margin: 32px 0 0; }
    footer { margin-top: 48px; color: #666; font-size: 0.9rem; border-top: 1px solid #ddd; padding-top: 16px; }
    a { color: #0b57d0; }
"""


def mb(n: int) -> str:
    return f"{n / 1_048_576:.1f} MB"


def datos(t: dict, d: dict) -> str:
    return (f'<p class="datos">{t["version"]} {html.escape(d["version"])} · {t["tamano"]} {mb(d["bytes"])}<br>'
            f'{t["sha"]}: <code>{d["sha256"].lower()}</code></p>')


def pagina(idioma: str, descargas: dict) -> str:
    t, a, w = T[idioma], descargas["android"], descargas["windows"]
    arriba = "../" if idioma == "es" else "../../"
    idiomas = " · ".join(f"<strong>{n}</strong>" if c == idioma else
                         f'<a href="{SITIO}/descargar/{"" if c == "es" else c + "/"}" lang="{c}" hreflang="{c}">{n}</a>' for c, n in NOMBRES.items())
    alternos = "\n".join(f'  <link rel="alternate" hreflang="{c}" href="{SITIO}/descargar/{"" if c == "es" else c + "/"}">' for c in NOMBRES)
    marcas = "\n".join(f"      <details><summary>{html.escape(m)}</summary><ol>" + "".join(f"<li>{p}</li>" for p in pasos) + "</ol></details>"
                       for m, pasos in t["marcas"].items())
    qr = (f'  <div class="qr"><img src="{SITIO}/descargar/qr.svg" alt="QR"><p>{t["qr"]}</p></div>\n'
          if (RAIZ / "descargar" / "qr.svg").exists() else "")
    n1, n2 = (f'{t["paso"]} 1', f'{t["paso"]} 2') if idioma != "zh" else ("第 1 步", "第 2 步")
    return f"""<!DOCTYPE html>
<html lang="{idioma}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["titulo"]}</title>
  <meta name="description" content="{html.escape(t["desc"])}">
{alternos}
  <style>{CSS}  </style>
</head>
<body>
<main>
  <p class="idiomas">{idiomas}</p>
  <h1>{t["titulo"]}</h1>
  <p class="sub">{t["sub"]}</p>
{qr}
  <h2 id="android">{t["android"]}</h2>
  <a class="boton" href="{a["url"]}">{t["bajar_apk"]}</a>
  {datos(t, a)}
  <ol>
    <li>{t["a1"]}</li>
    <li>{t["a2"]}</li>
    <li>{t["a3"]}
{marcas}
    </li>
    <li>{t["a4"]}</li>
    <li>{t["a5"]}</li>
  </ol>

  <h2 id="windows">{t["windows"]}</h2>
  <a class="boton" href="{w["url"]}">{t["bajar_exe"]}</a>
  {datos(t, w)}
  <ol>
    <li>{t["w1"].format(exe=html.escape(w["archivo"]))}</li>
    <li>{t["w2"]}
      <div class="pantallas">
        <div class="ss"><small>{n1}</small><b>{t["ss_titulo"]}</b>{t["ss_texto"]}<br><u class="marca">{t["ss_mas"]}</u><div class="fila"><span>{t["ss_no"]}</span></div></div>
        <div class="ss"><small>{n2}</small><b>{t["ss_titulo"]}</b>{t["ss_texto"]}<div class="fila"><span class="marca">{t["ss_ejecutar"]}</span><span>{t["ss_no"]}</span></div></div>
      </div>
    </li>
    <li>{t["w3"]}</li>
  </ol>

  <h2>{t["activar"]}</h2>
  <p>{t["activar_texto"]}</p>

  <h2>{t["comprobar"]}</h2>
  <p>{t["comprobar_texto"]}</p>

  <div class="aviso">{t["aviso"]}</div>
  <footer>© 2026 YappyVoz · <a href="{arriba}">{t["inicio"]}</a> · <a href="{arriba}privacidad/{"" if idioma == "es" else idioma + "/"}">{t["privacidad"]}</a></footer>
</main>
</body>
</html>
"""


def main() -> int:
    descargas = json.loads((RAIZ / "descargas.json").read_text("utf-8"))
    mal = []
    for idioma, ruta in RUTAS.items():
        destino, texto = RAIZ / ruta, pagina(idioma, descargas)
        if "--comprobar" in sys.argv:
            if not destino.exists() or destino.read_text("utf-8") != texto:
                mal.append(ruta)
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, "utf-8", newline="\n")
    if mal:
        print("No coinciden con descargas.json (ejecute tools/generar_descargar.py):", ", ".join(mal))
        return 1
    print("descargar: 3 páginas", "comprobadas" if "--comprobar" in sys.argv else "escritas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
