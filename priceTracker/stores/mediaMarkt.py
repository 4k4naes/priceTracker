from playwright.sync_api import sync_playwright

def get_price_mediamarkt(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            locale="pl-PL",
        )
        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector("span.sc-e0c7d9f7-0.bPkjPs", timeout=20000)

        spans = page.locator("span.sc-e0c7d9f7-0.bPkjPs").all_inner_texts()

        price_raw = next((s for s in spans if "zł" in s), None)

        browser.close()

        if not price_raw:
            print("niema ceny")
            return None

        clean_price = (
            price_raw.replace("zł", "")
            .replace(",", ".")
            .replace(" ", "")
            .strip()
        )

        return float(clean_price)

url = input("URL:")
print(get_price_mediamarkt(url))
