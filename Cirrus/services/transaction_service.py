from playwright.async_api import expect


class TransactionService:

    def __init__(self, page):
        self.page = page

    async def wait_for_new_transaction(self):

        transaction_locator = self.page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
        )

        old_transaction_id = (
            await transaction_locator.text_content()
        ).strip()

        max_attempts = 11

        for attempt in range(max_attempts):

            print(
                f"Waiting for transaction update "
                f"({attempt + 1}/{max_attempts})..."
            )

            await self.page.wait_for_timeout(
                30000
            )

            await self.page.reload(
                wait_until="networkidle"
            )

            latest_transaction = self.page.locator(
                'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
            )

            new_transaction_id = (
                await latest_transaction.text_content()
            ).strip()

            if new_transaction_id != old_transaction_id:
                print(
                    f"New Transaction Found : "
                    f"{new_transaction_id}"
                )
                return

        raise Exception(
            "No new transaction generated "
            "within expected time"
        )

    async def get_details(self):

        transaction_name = self.page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[1]'
        )

        transaction_name = (
            await transaction_name.text_content()
        ).replace(
            " - response",
            ""
        ).strip()

        transaction_id = self.page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
        )

        transaction_id = (
            await transaction_id.text_content()
        ).strip()

        timestamp = self.page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/p[1]'
        )

        timestamp = (
            await timestamp.text_content()
        ).strip()

        status = self.page.locator(
            'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[2]/div/span'
        )

        status = (
            await status.text_content()
        ).strip()

        return {
            "name": transaction_name,
            "id": transaction_id,
            "timestamp": timestamp,
            "status": status
        }

    async def open_payload(self):

        await self.page.get_by_text(
            "View Payload",
            exact=True
        ).first.click()

    async def close_payload(self):

        try:

            await self.page.keyboard.press(
                "Escape"
            )

            await self.page.wait_for_timeout(
                2000
            )

        except Exception:
            pass