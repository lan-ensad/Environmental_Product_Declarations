import os
import asyncio
from playwright.async_api import async_playwright
import aiohttp

os.makedirs("docs", exist_ok=True)

async def download_pdf(session, url, output_path):
    if os.path.exists(output_path):
        print(f"Already existing file : {output_path}")
        return
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(output_path, "wb") as f:
                    f.write(await resp.read())
                print(f"Downloded : {output_path}")
            else:
                print(f"Erreur ({resp.status}) pour : {url}")
    except Exception as e:
        print(f"Exception {url}: {e}")

async def extract_pdfs_from_page(page):
    await page.wait_for_selector("a[href$='.pdf']")
    return await page.eval_on_selector_all("a[href$='.pdf']", "els => els.map(e => e.href)")

async def main():
    pdf_urls = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.labelingsustainability.com/holcim-epds", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        while True:
            print("Scraping page...")
            new_pdfs = await extract_pdfs_from_page(page)
            pdf_urls.update(new_pdfs)

            next_button = await page.query_selector('[data-testid="Pagination_NavButton_Next"]')
            if not next_button:
                print("No more Next button")
                break
            if await next_button.get_attribute("aria-disabled") == "true":
                print("Last page reach")
                break

            print("Next page...")
            await next_button.click()
            await page.wait_for_timeout(3000)

        await browser.close()

    print(f"{len(pdf_urls)} PDF found. Downloading missing files...")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in pdf_urls:
            filename = os.path.basename(url.split("?")[0])
            output_path = os.path.join("docs", filename)
            tasks.append(download_pdf(session, url, output_path))
        await asyncio.gather(*tasks)

asyncio.run(main())
