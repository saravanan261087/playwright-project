import asyncio

from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:

        #operation_name = input("Enter operation name: ")

        browser = await p.chromium.launch(
            channel="chrome",
            headless=False
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
            ignore_https_errors=True
        )

        page = await context.new_page()

        # Open device page
        await page.goto(
            "https://10.41.177.62:8443/device/88-73-84-54-00-02-D3-1A",
             wait_until="networkidle"
        )
        first_event = page.get_by_role("listitem").first

        await expect(first_event).to_be_visible()
        print(f"Current Transaction: {first_event}")

    if __name__ == "__main__":
        asyncio.run(main())

