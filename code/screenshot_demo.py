from playwright.sync_api import sync_playwright
import time

SCREENSHOT_DIR = "x:/workspace/Paper/competitions/0G-APAC-Hackathon/docs"
EXAMPLE_DIR = "x:/workspace/Paper/competitions/0G-APAC-Hackathon/code/example_images"

p = sync_playwright().start()
b = p.chromium.launch()
page = b.new_page(viewport={"width": 1440, "height": 900})
page.goto("http://127.0.0.1:7861", timeout=30000)
page.wait_for_timeout(3000)

upload = page.query_selector("input[type=file]")
if upload:
    upload.set_input_files(f"{EXAMPLE_DIR}/true1_real.jpg")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{SCREENSHOT_DIR}/screenshot_uploaded.png", full_page=True)
    print("Uploaded screenshot saved")

    btns = page.query_selector_all("button")
    analyze_btn = None
    for btn in btns:
        text = btn.inner_text()
        if "Analyze" in text:
            analyze_btn = btn
            break

    if analyze_btn:
        analyze_btn.click()
        page.wait_for_timeout(10000)
        page.screenshot(path=f"{SCREENSHOT_DIR}/screenshot_result_true1.png", full_page=True)
        print("Result screenshot (true1) saved")

        upload2 = page.query_selector("input[type=file]")
        if upload2:
            upload2.set_input_files(f"{EXAMPLE_DIR}/false1_ai_generated.png")
            page.wait_for_timeout(2000)
            if analyze_btn:
                analyze_btn.click()
                page.wait_for_timeout(10000)
                page.screenshot(path=f"{SCREENSHOT_DIR}/screenshot_result_false1.png", full_page=True)
                print("Result screenshot (false1) saved")
    else:
        print("Analyze button not found")
else:
    print("File input not found")

b.close()
p.stop()
