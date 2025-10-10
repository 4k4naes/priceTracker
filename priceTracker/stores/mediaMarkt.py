from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def get_price_mediamarkt(url: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
                locale="pl-PL",
            )
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except PlaywrightTimeoutError:
                print("Nie udało odnalezc sie strony.")
                return None

            try:
                page.wait_for_selector("span.sc-e0c7d9f7-0.bPkjPs", state="attached", timeout=20000)
            except PlaywrightTimeoutError:
                print("Nie znaleziono elementu.")
                return None

            spans = page.locator("span.sc-e0c7d9f7-0.bPkjPs").all_inner_texts()
            price_raw = next((s for s in spans if "zł" in s), None)

            browser.close()

            if not price_raw:
                print("Nie znaleziono ceny na stronie.")
                return None

            clean_price = (
                price_raw.replace("zł", "")
                .replace(",", ".")
                .replace(" ", "")
                .strip()
            )

            if clean_price is not None:
                return float(clean_price)
            else:
                print("Nie odnaleziono ceny")
                return None

                        

    except Exception as e:
        print(f"Nieoczekiwany błąd ({type(e).__name__}): {e}")
        return None