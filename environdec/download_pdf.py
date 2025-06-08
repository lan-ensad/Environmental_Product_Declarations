import asyncio
import json
import os
from pathlib import Path
import aiohttp
from playwright.async_api import async_playwright

URLS_FILE = "urls.jsonl"
DOWNLOAD_DIR = "docs"

def load_urls():
    urls = []
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                url = data.get("url")
                if url:
                    urls.append(url)
            except json.JSONDecodeError:
                continue
    return urls

async def download_file(session, url, dest_path):
    async with session.get(url) as resp:
        if resp.status == 200:
            with open(dest_path, "wb") as f:
                f.write(await resp.read())
            print(f"Downloaded to {dest_path}")
        else:
            raise Exception(f"HTTP {resp.status} while downloading {url}")

async def download_pdfs():
    Path(DOWNLOAD_DIR).mkdir(exist_ok=True)
    urls = load_urls()

    async with aiohttp.ClientSession() as session:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            for url in urls:
                try:
                    epd_id = url.rstrip("/").split("/")[-1]
                    filename = f"{epd_id}.pdf"
                    dest_path = os.path.join(DOWNLOAD_DIR, filename)

                    if os.path.exists(dest_path):
                        print(f"Skipping {filename} (already exists)")
                        continue

                    print(f"Visiting {url}")
                    await page.goto(url, timeout=60000)

                    await page.wait_for_selector('a:has-text(".pdf")', timeout=10000)
                    link = page.locator('a:has-text(".pdf")').first
                    href = await link.get_attribute("href")
                    if not href.startswith("http"):
                        href = "https://environdec.com" + href

                    print(f"Downloading from {href} -> {filename}")
                    await download_file(session, href, dest_path)

                except Exception as e:
                    print(f"Error with {url}: {e}")

            await browser.close()

if __name__ == "__main__":
    asyncio.run(download_pdfs())
