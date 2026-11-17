import os

class PayloadService:

    @staticmethod
    async def save_payload(
            page,
            output_folder,
            transaction_name):

        await page.get_by_text(
            "View Payload",
            exact=True
        ).first.click()

        dialog = page.get_by_role(
            "dialog"
        )

        payload = \
            await dialog.inner_text()

        file_name = os.path.join(
            output_folder,
            f"{transaction_name}_payload.txt"
        )

        with open(
                file_name,
                "w",
                encoding="utf-8") as f:

            f.write(payload)

        return file_name