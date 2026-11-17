import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture
async def page():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            channel="chrome",
            headless=True
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\Cirrus\auth\auth.json",
            ignore_https_errors=True
        )

        page = await context.new_page()

        yield page

        await context.close()
        await browser.close()