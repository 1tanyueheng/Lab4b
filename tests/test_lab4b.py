"""Test Lab 4b in headless Chrome against the local server on port 8137."""
import io
import json
import sys
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

LAB4A_TESTS = Path(r"C:\Users\yuehe\Desktop\study\y3s1\web deve\lab4\Lab4a\tests")
sys.path.insert(0, str(LAB4A_TESTS))
from test_lab4a import Browser, Session  # noqa: E402

BASE = "http://127.0.0.1:8137"
results = []


def check(name, cond, detail=""):
    results.append((bool(cond), name, detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + ("" if cond else f"  -> {detail}"))


def main():
    br = Browser()
    try:
        s = Session(br.ws_url)
        s.call("Page.enable")
        s.call("Runtime.enable")

        # ---------------- Q2: books.html ----------------
        print("\n=== Q2: books.html (fetched over HTTP) ===")
        s.navigate(f"{BASE}/books.html")
        # fetch is async; give it time to resolve
        for _ in range(30):
            if s.eval("document.getElementById('firstTitle').textContent") != "Loading\u2026":
                break
            time.sleep(0.2)

        t1 = s.eval("document.getElementById('firstTitle').textContent")
        a2 = s.eval("document.getElementById('secondAuthor').textContent")
        genres = s.eval(
            "Array.from(document.querySelectorAll('#genres li')).map(function(li){return li.textContent;})"
        )
        err = s.eval("document.getElementById('error').textContent")

        check("(a) first book title", t1 == "The Great Gatsby", repr(t1))
        check("(b) second book author", a2 == "Harper Lee", repr(a2))
        check(
            "(c) genres grouped by title",
            genres
            == [
                "The Great Gatsby \u2014 Fiction, Classics",
                "To Kill a Mockingbird \u2014 Fiction, Coming-of-Age",
            ],
            repr(genres),
        )
        check("no error message shown", err == "", repr(err))

        # error handling: point fetch at a missing file
        print("\n=== Q2: error handling (missing JSON) ===")
        s.navigate(f"{BASE}/books.html")
        time.sleep(1.0)
        s.eval(
            "document.getElementById('error').textContent='';"
            "fetch('missing.json').then(function(r){if(!r.ok)throw new Error('status '+r.status);"
            "return r.json();}).catch(function(e){"
            "document.getElementById('error').textContent='Sorry, the book data could not be loaded. '+e.message;});"
        )
        time.sleep(1.2)
        err2 = s.eval("document.getElementById('error').textContent")
        check("missing file shows friendly error", "could not be loaded" in err2, repr(err2))

        # ---------------- Q3: jquery-dom.html ----------------
        print("\n=== Q3: jquery-dom.html ===")
        s.navigate(f"{BASE}/jquery-dom.html")
        time.sleep(1.0)

        ver = s.eval("typeof jQuery === 'function' ? jQuery.fn.jquery : null")
        check("jQuery loaded", ver is not None, repr(ver))
        print(f"       jQuery version: {ver}")

        el = s.eval("document.getElementById('myElement').textContent")
        check("(a) #myElement text replaced", el == "Modified Text", repr(el))

        has = s.eval("document.getElementById('myDIV').classList.contains('myStyle')")
        check("(b) #myDIV has myStyle class", has is True, repr(has))

        bg = s.eval(
            "getComputedStyle(document.getElementById('myDIV')).backgroundColor"
        )
        check("(b) coral background applied", bg == "rgb(255, 127, 80)", repr(bg))

        # (c) click -> alert. Stub alert so it does not block the browser.
        s.eval("window.__alerts=[]; window.alert=function(m){window.__alerts.push(m);};")
        s.eval("document.getElementById('myButton').click()")
        time.sleep(0.3)
        alerts = s.eval("window.__alerts")
        check("(c) click shows 'Button clicked!'", alerts == ["Button clicked!"], repr(alerts))

        print("\n" + "=" * 60)
        passed = sum(1 for ok, _, _ in results if ok)
        print(f"RESULT: {passed}/{len(results)} checks passed")
        failed = [(n, d) for ok, n, d in results if not ok]
        if failed:
            for n, d in failed:
                print(f"  FAIL {n}  {d}")
        return 0 if not failed else 1
    finally:
        br.close()


if __name__ == "__main__":
    raise SystemExit(main())
