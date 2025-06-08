import asyncio
import json
import os
from playwright.async_api import async_playwright

OUTPUT_FILE = "urls.jsonl"
SEARCH_TERM = "Holcim"
SEARCH_URL = "https://environdec.com/library"

def load_existing_urls():
    if not os.path.exists(OUTPUT_FILE):
        return set()

    seen = set()
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                url = data.get("url")
                if url:
                    seen.add(url)
            except json.JSONDecodeError:
                continue
    return seen

async def save_url_to_jsonl(url, seen):
    if url not in seen:
        seen.add(url)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            json.dump({"url": url}, f)
            f.write("\n")
        print(f"Saved: {url}")

async def scroll_to_load_all(page, selector, seen):
    stable_rounds = 0
    previous_hrefs = set()

    while stable_rounds < 3: # 3 trys to load more links
        elements = await page.query_selector_all(selector)
        current_hrefs = {await el.get_attribute("href") for el in elements if await el.get_attribute("href")}

        if current_hrefs != previous_hrefs:
            print(f"New DOM state detected ({len(current_hrefs)} links)")
            stable_rounds = 0
        else:
            stable_rounds += 1
            print(f"No change in DOM ({stable_rounds}/3)")

        new_hrefs = current_hrefs - seen
        for href in new_hrefs:
            full_url = f"https://environdec.com{href}"
            await save_url_to_jsonl(full_url, seen)

        previous_hrefs = current_hrefs

        if elements:
            await elements[-1].scroll_into_view_if_needed()
            await page.wait_for_timeout(2000)
        else:
            break

async def run():
    seen = load_existing_urls()
    print(f"Loaded {len(seen)} existing URLs from {OUTPUT_FILE}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(SEARCH_URL)

        await page.fill('input[placeholder*="company name"]', SEARCH_TERM)
        await page.keyboard.press("Enter")
        await page.wait_for_selector('a[href^="/library/"]')

        await scroll_to_load_all(page, 'a[href^="/library/"]', seen)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
