import asyncio
import pyautogui
from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:


        browser = await p.chromium.launch(
            channel="chrome",
            headless=False
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
            ignore_https_errors=True
        )

        page = await context.new_page()
        await page.goto(
            "https://10.41.177.62:8443/device/88-73-84-54-00-02-D3-1A"
        )

        # Zoom out
        pyautogui.hotkey("ctrl", "-")
        pyautogui.hotkey("ctrl", "-")
        pyautogui.hotkey("ctrl", "-")

        # Run Operation
        run_operation_btn = page.locator(
            "xpath=/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/button"
        )

        await expect(run_operation_btn).to_be_visible()
        await run_operation_btn.click()

        # Search operation

        operation_name = "wanInterfaceSelfDiagnosis"

        operation_input = page.locator("#name")

        await expect(operation_input).to_be_visible()
        await operation_input.fill(operation_name)

        await page.wait_for_timeout(3000)

        await page.get_by_role(
            "button",
            name=operation_name
        ).click()

        # Deploy
        deploy_btn = page.get_by_role(
            "button",
            name="Deploy"
        )

        await expect(deploy_btn).to_be_enabled()
        await deploy_btn.click()

        await page.wait_for_timeout(3000)

        # Confirm Deployment
        confirm_btn = page.locator(
            "xpath=/html/body/div[8]/div/div/div/div[2]/div[2]/div[2]/button[1]"
        )

        await expect(confirm_btn).to_be_visible()
        await confirm_btn.click()

        # Close popup if present
        try:
            close_btn = page.get_by_role(
                "button",
                name="Close"
            )

            if await close_btn.is_visible():
                await close_btn.click()

        except Exception:
            pass

        await page.wait_for_timeout(15000)

        # Capture current transaction
        old_transaction = await (
            page.locator("tbody tr")
            .first
            .locator("td")
            .nth(0)
            .text_content()
        )

        print(f"Current Transaction: {old_transaction}")

        await page.wait_for_timeout(60000)

        # Refresh
        try:
            refresh_btn = page.locator(
                "xpath=/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/div[1]/div[2]/button"
            )

            await refresh_btn.click()

        except Exception:
            print("Refresh button not found")

        # Wait until top transaction changes
        await expect(
            page.locator("tbody tr")
            .first
            .locator("td")
            .nth(0)
        ).not_to_have_text(
            old_transaction,
            timeout=60000
        )

        print("✅ New transaction detected")

        # Latest row
        latest_row = page.locator("tbody tr").first

        await expect(latest_row).to_be_visible(
            timeout=60000
        )

        transaction_id = await latest_row.locator("td").nth(0).text_content()
        timestamp = await latest_row.locator("td").nth(1).text_content()
        task = await latest_row.locator("td").nth(2).text_content()
        operation = await latest_row.locator("td").nth(3).text_content()
        status = await latest_row.locator("td").nth(4).text_content()

        print("\n===== Latest Transaction =====")
        print(f"Transaction ID : {transaction_id}")
        print(f"Timestamp      : {timestamp}")
        print(f"Task           : {task}")
        print(f"Operation      : {operation}")
        print(f"Status         : {status}")
        print("==============================")

        # Validation
        if status and status.strip().upper() == "SUCCESS":
            print(f"✅ Operation '{operation}' completed successfully")
        else:
            print(f"❌ Operation '{operation}' failed")
            print(f"Current Status: {status}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())