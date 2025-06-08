import os
import asyncio
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright

DOWNLOAD_DIR = os.path.join(os.getcwd(), "docs")

async def download_pdfs():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        print("Searching...")
        await page.goto("https://www.holcim.us/technical-specifications", wait_until="networkidle")

        # Search for PDF links
        pdf_links = await page.eval_on_selector_all(
            'a[href$=".pdf"]',
            "links => links.map(link => link.href)"
        )

        print(f"{len(pdf_links)} PDF found")

        for link in pdf_links:
            filename = unquote(os.path.basename(urlparse(link).path))
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            if os.path.exists(filepath):
                print(f"Already exist : {filename}")
                continue

            print(f"Downloading : {filename}")

            # Wainting for download
            async with page.expect_download() as download_info:
                await page.evaluate("url => window.open(url)", link)

            download = await download_info.value
            await download.save_as(filepath)

        await browser.close()
        print("All done")

if __name__ == "__main__":
    asyncio.run(download_pdfs())
