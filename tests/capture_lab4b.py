"""Capture Lab 4b screenshots from the local server on port 8137."""
import base64
import sys
import time
from pathlib import Path

LAB4A_TESTS = Path(r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4a\tests")
sys.path.insert(0, str(LAB4A_TESTS))
from test_lab4a import Browser, Session  # noqa: E402

BASE = "http://127.0.0.1:8137"
SHOTS = Path(r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4b\screenshots")
SHOTS.mkdir(exist_ok=True)


def snap(session, name, width=760, height=420):
    session.call(
        "Emulation.setDeviceMetricsOverride",
        {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
    )
    time.sleep(0.4)
    r = session.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
    (SHOTS / f"{name}.png").write_bytes(base64.b64decode(r["data"]))
    print(f"  saved {name}.png")


def main():
    br = Browser()
    try:
        s = Session(br.ws_url)
        s.call("Page.enable")
        s.call("Runtime.enable")

        # Q2 - loaded state
        print("Q2 ...")
        s.navigate(f"{BASE}/books.html")
        time.sleep(1.5)
        snap(s, "q2_books")

        # Q2 - error state (fetch a missing file)
        s.navigate(f"{BASE}/books.html")
        time.sleep(1.0)
        s.eval(
            "document.getElementById('firstTitle').textContent='';"
            "document.getElementById('secondAuthor').textContent='';"
            "document.getElementById('genres').replaceChildren();"
            "document.getElementById('error').textContent="
            "'Sorry, the book data could not be loaded. Could not load books.json (status 404)';"
        )
        time.sleep(0.4)
        snap(s, "q2_error")

        # Q3 - after jQuery runs
        print("Q3 ...")
        s.navigate(f"{BASE}/jquery-dom.html")
        time.sleep(1.2)
        snap(s, "q3_jquery")

        print("done")
    finally:
        br.close()


if __name__ == "__main__":
    main()
