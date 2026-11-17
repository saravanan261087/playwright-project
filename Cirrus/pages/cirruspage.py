from playwright.async_api import expect
from config.settings import BASE_URL


class CirrusPage:

    def __init__(self, page):
        self.page = page

    async def open_device(
        self,
        guid
    ):
        await self.page.goto(
            f"{BASE_URL}/device/{guid}",
            wait_until="networkidle",
            timeout=60000
        )

    async def open_operation_window(self):

        try:
            await self.page.keyboard.press(
                "Escape"
            )
        except Exception:
            pass

        run_button = self.page.get_by_role(
            "button",
            name="Run Operation"
        )

        await expect(
            run_button
        ).to_be_visible(
            timeout=60000
        )

        await run_button.click()

        operation_input = self.page.locator(
            "#name"
        )

        await expect(
            operation_input
        ).to_be_visible(
            timeout=60000
        )

    async def select_operation(
        self,
        operation_name
    ):

        operation_input = self.page.locator(
            "#name"
        )

        await operation_input.clear()

        await operation_input.fill(
            operation_name
        )

        await self.page.wait_for_timeout(
            6000
        )

        await self.page.get_by_role(
            "button",
            name=operation_name
        ).click()

    async def deploy_operation(self):

        deploy_btn = self.page.get_by_role(
            "button",
            name="Deploy"
        )

        await expect(
            deploy_btn
        ).to_be_enabled()

        await deploy_btn.click()

        await self.page.wait_for_timeout(
            30000
        )

        dialog = self.page.get_by_role(
            "dialog"
        )

        confirm_btn = dialog.get_by_role(
            "button",
            name="Deploy",
            exact=True
        )

        await expect(
            confirm_btn
        ).to_be_visible(
            timeout=10000
        )

        await confirm_btn.click()

        try:

            close_btn = self.page.get_by_role(
                "button",
                name="Close"
            )

            if await close_btn.is_visible():
                await close_btn.click()

        except Exception:
            pass