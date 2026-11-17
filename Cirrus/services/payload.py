import os
from playwright.async_api import expect


class PayloadService:

    @staticmethod
    async def save_payload(
        page,
        output_folder,
        transaction_name
    ):

        await page.get_by_text(
            "View Payload",
            exact=True
        ).first.click()

        dialog = page.get_by_role(
            "dialog"
        )

        await expect(
            dialog
        ).to_be_visible()

        payload_text = await dialog.inner_text()

        payload_file = os.path.join(
            output_folder,
            f"{transaction_name}_payload.txt"
        )

        with open(
            payload_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(payload_text)

        # CRITICAL
        try:
            await page.keyboard.press(
                "Escape"
            )

            await page.wait_for_timeout(
                2000
            )

        except Exception:
            pass

        return payload_file