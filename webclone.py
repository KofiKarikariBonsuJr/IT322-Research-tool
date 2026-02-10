#!/usr/bin/env python3

import argparse
import os
import sys
import base64
from playwright.sync_api import sync_playwright
from openai import OpenAI
from PIL import Image

SCREENSHOT_FILE = "screenshot.png"
HTML_FILE = "recreated.html"

MODEL = "gpt-4.1-mini"  # Vision-capable


def capture_screenshot(url, output):
    print("📸 Capturing screenshot...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=output, full_page=True)
        browser.close()


def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_html_from_image(image_path):
    print("🧠 Reconstructing HTML with AI...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    image_b64 = image_to_base64(image_path)

    prompt = """
You are a frontend engineer.

Given a screenshot of a website, recreate the page as clean,
semantic HTML5 with embedded CSS.

Requirements:
- Use modern HTML5 elements
- Recreate layout, colors, spacing, and typography
- Use inline <style> CSS
- Do NOT include JavaScript
- Approximate fonts if unknown
- Make it responsive
- Output ONLY valid HTML
"""

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_base64": image_b64,
                    },
                ],
            }
        ],
    )

    return response.output_text


def save_html(html):
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description="Website Screenshot + AI HTML Reconstruction Tool"
    )
    parser.add_argument("url", help="URL to capture and recreate")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Missing OPENAI_API_KEY")
        sys.exit(1)

    capture_screenshot(args.url, SCREENSHOT_FILE)
    html = generate_html_from_image(SCREENSHOT_FILE)
    save_html(html)

    print("\n✅ Done!")
    print(f"📸 Screenshot saved to: {SCREENSHOT_FILE}")
    print(f"🧱 HTML saved to: {HTML_FILE}")


if __name__ == "__main__":
    main()
