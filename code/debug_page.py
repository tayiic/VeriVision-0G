"""Debug Gradio page structure for Playwright selectors"""
import subprocess, sys, time, os
import logging

logger = logging.getLogger(__name__)


# Start Gradio
env = os.environ.copy()
env["VERIVISION_DEMO"] = "1"
proc = subprocess.Popen(
    [sys.executable, "gradio_app.py"],
    cwd=os.path.dirname(__file__),
    env=env,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)

# Wait for startup
for _ in range(20):
    try:
        import urllib.request
        urllib.request.urlopen("http://127.0.0.1:7861", timeout=2)
        break
    except Exception as exc:
        logging.warning('caught bare except: %s', exc, exc_info=True)
        time.sleep(1.5)
else:
    print("Gradio didn't start")
    proc.terminate()
    sys.exit(1)

print("Gradio running, analyzing page...")

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1280, "height": 720})
    page.goto("http://127.0.0.1:7861", timeout=15000)
    page.wait_for_timeout(4000)

    # Find all inputs
    for el in page.locator('input').all():
        t = el.get_attribute('type') or 'text'
        name = el.get_attribute('name') or ''
        label = el.get_attribute('aria-label') or ''
        print(f"input[type={t}] name={name} label={label}")

    # Find all buttons
    for btn in page.locator('button').all():
        print(f"button: {btn.inner_text()[:100]}")

    # Find file upload elements (Gradio uses specific markup)
    for el in page.locator('[data-testid], .file-preview, input[type=file]').all():
        print(f"upload el: tag={el.evaluate('el => el.tagName')} id={el.get_attribute('id')} class={el.get_attribute('class')}")

    # Also look for the upload button/label pattern
    html = page.content()
    # Find file-related elements
    import re
    for m in re.finditer(r'<(?:input|label|div)[^>]*file[^>]*>', html, re.I):
        snippet = m.group()[:120]
        print(f"FILE-RELATED: {snippet}")

    b.close()

proc.terminate()
proc.wait()
print("Done")
