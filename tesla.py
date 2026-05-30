# Search for 'chirag gajra' on LinkedIn
# Estimated duration: 10s · 5 steps
# Run with: python script.py
# Install: pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

    # Navigate to LinkedIn
    page.goto("https://www.linkedin.com", wait_until="domcontentloaded")

    # Wait for the page to load
    page.wait_for_load_state("networkidle")

    # Type 'chirag gajra' into the search bar
    page.fill("input[aria-label=\"Search\"]", "chirag gajra")

    # Press Enter to perform the search
    page.keyboard.press("Enter")

    # Wait for search results to load
    page.wait_for_load_state("networkidle")

        browser.close()


if __name__ == "__main__":
    main()


    # Wait for search results to load
    page.wait_for_load_state("networkidle")

    # Click the first search result
    page.click("h3")

        browser.close()


if __name__ == "__main__":
    main()
