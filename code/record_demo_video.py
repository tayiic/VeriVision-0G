"""
Automated demo video recording for VeriVision.
Starts Gradio in background, walks through full demo, outputs demo_video.webm (~3 min)
"""
import subprocess
import sys
import time
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)


GRADIO_URL = "http://127.0.0.1:7861"
VIDEO_DIR = Path(__file__).parent.parent / "docs" / "demo_video"
EXAMPLE_DIR = Path(__file__).parent / "example_images"
OUTPUT = Path(__file__).parent.parent / "docs" / "demo_video.webm"
EXPLORER_URL = "https://chainscan-galileo.0g.ai/address/0xbDc0C48958267F00745A2c114C96A0016DA4003B"
GITHUB_URL = "https://github.com/tayiic/VeriVision-0G"


def start_gradio():
    env = os.environ.copy()
    env["VERIVISION_DEMO"] = "1"
    proc = subprocess.Popen(
        [sys.executable, "gradio_app.py"],
        cwd=Path(__file__).parent,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(25):
        try:
            import urllib.request
            urllib.request.urlopen(GRADIO_URL, timeout=2)
            print("Gradio started")
            return proc
        except Exception as exc:
            logging.warning('caught bare except: %s', exc, exc_info=True)
            time.sleep(1.5)
    proc.terminate()
    raise RuntimeError("Gradio failed to start")


def record_demo():
    gradio_proc = start_gradio()

    try:
        # Clean up previous runs
        if VIDEO_DIR.exists():
            shutil.rmtree(str(VIDEO_DIR))
        VIDEO_DIR.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(VIDEO_DIR),
                record_video_size={"width": 1280, "height": 720},
            )
            page = context.new_page()

            def upload_image(img_path):
                upload_area = page.locator("button", has_text="Click to Upload")
                upload_area.click()
                page.wait_for_timeout(800)
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(img_path, timeout=10000)
                page.wait_for_timeout(2000)

            # ============================================================
            # Scene 1: Landing page (0:00-0:25)
            # ============================================================
            page.goto(GRADIO_URL, timeout=20000)
            page.wait_for_timeout(3000)
            # Slowly scroll down to show architecture description
            page.evaluate("window.scrollTo(0, 200)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 500)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 800)")
            page.wait_for_timeout(3000)
            # Scroll back to top
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(3000)

            # ============================================================
            # Scene 2: Upload real photo + analyze + results (0:25-1:30)
            # ============================================================
            upload_image(str(EXAMPLE_DIR / "true1_real.jpg"))
            page.wait_for_timeout(1500)

            analyze_btn = page.locator("button").filter(has_text="Analyze").first
            analyze_btn.click()
            page.wait_for_timeout(6000)  # Wait for demo analysis

            # Scroll through results slowly
            page.evaluate("window.scrollTo(0, 200)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 500)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(4000)

            # Scroll back up to show summary
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(2000)

            # ============================================================
            # Scene 3: Upload AI-generated image + results (1:30-2:15)
            # ============================================================
            upload_image(str(EXAMPLE_DIR / "false1_ai_generated.png"))
            page.wait_for_timeout(1500)
            analyze_btn.click()
            page.wait_for_timeout(6000)

            # Show results
            page.evaluate("window.scrollTo(0, 400)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(2000)

            # ============================================================
            # Scene 4: 0G Explorer - contract verification (2:15-2:40)
            # ============================================================
            page.goto(EXPLORER_URL, timeout=30000)
            page.wait_for_timeout(4000)
            # Scroll around
            page.evaluate("window.scrollTo(0, 300)")
            page.wait_for_timeout(3000)
            page.evaluate("window.scrollTo(0, 600)")
            page.wait_for_timeout(3000)

            # ============================================================
            # Scene 5: GitHub repository (2:40-3:00)
            # ============================================================
            page.goto(GITHUB_URL, timeout=30000)
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 300)")
            page.wait_for_timeout(3000)
            page.evaluate("window.scrollTo(0, 800)")
            page.wait_for_timeout(3000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(2000)

            # Close context to finalize video
            context.close()
            browser.close()

            # Find and copy video
            videos = list(VIDEO_DIR.glob("*.webm"))
            if videos:
                # Pick the correct video (there should be exactly one from this context)
                newest = max(videos, key=lambda p: p.stat().st_mtime)
                shutil.copy(newest, OUTPUT)
                size_mb = OUTPUT.stat().st_size / 1024 / 1024
                print(f"\nVideo saved: {OUTPUT}")
                print(f"Size: {size_mb:.1f} MB")
                if size_mb < 1:
                    print("WARNING: Video seems small - may be incomplete")
            else:
                print("ERROR: No video file produced")

    except Exception as e:
        print(f"Recording error: {e}")
        # Check if we still got a video
        videos = list(VIDEO_DIR.glob("*.webm"))
        if videos:
            newest = max(videos, key=lambda p: p.stat().st_mtime)
            shutil.copy(newest, OUTPUT)
            print(f"Partial video saved: {OUTPUT}")
    finally:
        gradio_proc.terminate()
        gradio_proc.wait()


if __name__ == "__main__":
    record_demo()
