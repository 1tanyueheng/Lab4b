"""Render evidence images for Lab 4b: the JSON file, its parse check, and the alert."""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

LAB4A_TESTS = Path(r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4a\tests")
sys.path.insert(0, str(LAB4A_TESTS))
from test_lab4a import Browser, Session  # noqa: E402

BASE = "http://127.0.0.1:8137"
LAB = Path(r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4b")
SHOTS = LAB / "screenshots"

# --- build an HTML page that shows the JSON file contents as code --------
raw = (LAB / "books.json").read_text(encoding="utf-8")
parsed = json.loads(raw)

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>books.json</title>
<link rel="stylesheet" href="style.css">
<style>
body {{ font-family: Consolas, monospace; }}
pre {{ background:#F1F1F1; border:1px solid #cccccc; border-left:6px solid #04AA6D;
      padding:16px; border-radius:4px; font-size:14px; line-height:1.55; overflow:auto; }}
.ok {{ color:#04AA6D; font-weight:bold; }}
</style></head>
<body>
<h1 style="font-family:Verdana,sans-serif">Question 1 &mdash; books.json</h1>
<pre>{raw.replace('&', '&amp;').replace('<', '&lt;')}</pre>
<p class="ok">&#10004; JSON parsed successfully &mdash; {len(parsed['books'])} books,
keys: {", ".join(parsed['books'][0].keys())}</p>
</body></html>"""

(LAB / "_json_evidence.html").write_text(html, encoding="utf-8")


def main():
    br = Browser()
    try:
        s = Session(br.ws_url)
        s.call("Page.enable")
        s.call("Runtime.enable")

        def snap(name, w=760, h=470):
            s.call("Emulation.setDeviceMetricsOverride",
                   {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False})
            time.sleep(0.4)
            r = s.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
            (SHOTS / f"{name}.png").write_bytes(base64.b64decode(r["data"]))
            print(f"  saved {name}.png")

        # Q1 - JSON file content + parse confirmation
        s.navigate(f"{BASE}/_json_evidence.html")
        time.sleep(0.6)
        snap("q1_json", 760, 470)

        # Q3 - alert evidence: capture the dialog via CDP Page.javascriptDialogOpening
        s.navigate(f"{BASE}/jquery-dom.html")
        time.sleep(1.0)
        s.call("Page.enable")
        # override alert to render a visible box so it appears in the screenshot
        s.eval(
            "window.alert=function(m){var d=document.createElement('div');"
            "d.id='alertBox';d.textContent=m;"
            "d.style.cssText='position:fixed;top:40px;left:50%;transform:translateX(-50%);"
            "background:#ffffff;border:1px solid #777;border-radius:6px;padding:18px 28px;"
            "font-weight:bold;box-shadow:0 4px 14px rgba(0,0,0,.3);z-index:99';"
            "document.body.appendChild(d);};"
        )
        s.eval("document.getElementById('myButton').click()")
        time.sleep(0.5)
        snap("q3_alert", 760, 420)
        print("done")
    finally:
        br.close()


if __name__ == "__main__":
    main()
