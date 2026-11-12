import asyncio

import pyautogui
from playwright.async_api import async_playwright


async def visit(page, url):
    try:
        await page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )
        print(f"Title: {await page.title()}")
    except Exception as e:
        print(f"Failed to load {url}: {e}")


async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            executable_path=r"C:\Users\chandrs4\Desktop\Chrome\chrome-win64\chrome-win64\chrome.exe",
            headless=False,
            args=["--ignore-certificate-errors"]
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
            ignore_https_errors=True
        )

        page1 = await context.new_page()
        page2 = await context.new_page()

        await asyncio.gather(
            visit(
                page1,
                "https://10.41.177.62:8443/device/88-73-84-54-00-02-D3-1A"
            ),
            visit(
                page2,
                "https://10.41.177.62:8443/device/88-73-84-84-00-2E-F1-70"
            )
        )
        pyautogui.hotkey("ctrl", "-")
        pyautogui.hotkey("ctrl", "-")
        pyautogui.hotkey("ctrl", "-")
        await page1.wait_for_timeout(15000)


        #await browser.close()


if __name__ == "__main__":
    asyncio.run(main())