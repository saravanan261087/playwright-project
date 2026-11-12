import asyncio

import pyautogui
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
            ignore_https_errors=True
        )

        page = await context.new_page()

        # Open device page
        await page.goto(
            "https://10.41.177.62:8443/device/88-73-84-54-00-02-D3-1A",

        )
        #pyautogui.hotkey("ctrl", "-")
        #pyautogui.hotkey("ctrl", "-")
        #pyautogui.hotkey("ctrl", "-")
        await page.evaluate("document.body.style.zoom='80%'")

        await page.wait_for_timeout(15000)

        refresh_btn = page.locator("button:has-text('Refresh')")

        if await refresh_btn.count() > 0:
            print("✅ Refresh button exists in DOM")

            if await refresh_btn.is_visible():
                print("✅ Refresh button is visible")
                await refresh_btn.click()
                print("✅ Refresh button is clicked")

            else:
                print("⚠️ Refresh button exists but is not visible")

                try:
                    await refresh_btn.scroll_into_view_if_needed()

                    if await refresh_btn.is_visible():
                        print("✅ Refresh button became visible after scrolling")
                        await refresh_btn.click()
                    else:
                        print("❌ Refresh button still not visible")

                except Exception as e:
                    print(f"❌ Scroll failed: {e}")

        else:
            print("❌ Refresh button not found")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())