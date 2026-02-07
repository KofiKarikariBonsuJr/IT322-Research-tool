#!/usr/bin/env python3

import argparse
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright


def safe_filename(url: str) -> str:
    name = re.sub(r"https?://", "", url)
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    return name.strip("_")[:60] + ".png"


async def take_screenshot(url: str, output: str, full_page: bool):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 1280, "height": 800}
        )

        print(f"🌐 Loading {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        print("📸 Taking screenshot...")
        await page.screenshot(
            path=output,
            full_page=full_page
        )

        await browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Website Screenshot CLI Tool"
    )
    parser.add_argument("url", help="Website URL to screenshot")
    parser.add_argument(
        "--out",
        help="Output file name (PNG)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Capture full page (default is viewport only)"
    )

    args = parser.parse_args()

    output = args.out or safe_filename(args.url)
    output_path = Path(output).resolve()

    asyncio.run(
        take_screenshot(
            args.url,
            str(output_path),
            args.full
        )
    )

    print(f"✅ Screenshot saved to: {output_path}")


if __name__ == "__main__":
    main()
