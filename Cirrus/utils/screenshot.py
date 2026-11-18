import os
class ScreenshotManager:

    @staticmethod
    async def capture(
            page,
            output_folder,
            transaction_name):

        # Latest transaction card
        latest_transaction = page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]'
        )

        # Scroll to latest transaction
        await latest_transaction.scroll_into_view_if_needed()

        # Allow UI to settle
        await page.wait_for_timeout(3000)

        screenshot_file = os.path.join(
            output_folder,
            f"{transaction_name}.png"
        )

        # Full page screenshot at current scroll position
        await page.screenshot(
            path=screenshot_file,
            full_page=True
        )

        print(
            f"Screenshot saved: "
            f"{screenshot_file}"
        )

        return screenshot_file