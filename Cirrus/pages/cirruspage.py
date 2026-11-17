from playwright.async_api import expect

from config.settings import BASE_URL
from config.locators import *


class CirrusPage:

    def __init__(self, page):

        self.page = page

    async def open_device(
            self,
            guid):

        await self.page.goto(
            f"{BASE_URL}/device/{guid}",
            wait_until="networkidle",
            timeout=60000
        )

    async def open_operation_window(self):

        btn = self.page.locator(
            RUN_OPERATION_BUTTON
        )

        await expect(btn).to_be_visible()

        await btn.click()

    async def select_operation(
            self,
            operation_name):

        operation_input = \
            self.page.locator("#name")

        await operation_input.fill(
            operation_name
        )

        await self.page.get_by_role(
            "button",
            name=operation_name
        ).click()

    async def deploy_operation(self):

        deploy_button = \
            self.page.get_by_role(
                "button",
                name="Deploy"
            )

        await deploy_button.click()

        dialog = \
            self.page.get_by_role(
                "dialog"
            )

        confirm = dialog.get_by_role(
            "button",
            name="Deploy",
            exact=True
        )

        await confirm.click()