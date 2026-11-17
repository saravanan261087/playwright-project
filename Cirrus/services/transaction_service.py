from config.locators import *
from config.settings import *


class TransactionService:

    def __init__(
            self,
            page):

        self.page = page

    async def wait_for_new_transaction(self):

        old_transaction = \
            await self.page.locator(
                TRANSACTION_ID
            ).text_content()

        old_transaction = \
            old_transaction.strip()

        for _ in range(
                TRANSACTION_WAIT_ATTEMPTS):

            await self.page.wait_for_timeout(
                TRANSACTION_WAIT_SECONDS * 1000
            )

            await self.page.reload()

            current = await \
                self.page.locator(
                    TRANSACTION_ID
                ).text_content()

            current = current.strip()

            if current != old_transaction:
                return current

        raise Exception(
            "New transaction not generated"
        )

    async def get_details(self):

        return {

            "id":
            (
                await self.page.locator(
                    TRANSACTION_ID
                ).text_content()
            ).strip(),

            "timestamp":
            (
                await self.page.locator(
                    TRANSACTION_TIMESTAMP
                ).text_content()
            ).strip(),

            "status":
            (
                await self.page.locator(
                    TRANSACTION_STATUS
                ).text_content()
            ).strip(),

            "name":
            (
                await self.page.locator(
                    TRANSACTION_NAME
                ).text_content()
            ).replace(
                " - response",
                ""
            )
        }