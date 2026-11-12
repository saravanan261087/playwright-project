import asyncio
import os
import sys
import psycopg2
import requests
from playwright.async_api import async_playwright, expect
from datetime import datetime

def check_vpn():
    """Check if VPN/Internal application is reachable."""
    try:
        response = requests.get(
            "https://10.41.177.62:8443",
            verify=False,
            timeout=10
        )

        print(f"✅ VPN Connected - Status Code: {response.status_code}")
        return True

    except Exception as e:
        #print(f"❌ VPN NOT Connected")
        return False

async def main():
    if not check_vpn():
        print("Execution stopped because VPN is not connected.")
        sys.exit(1)
    async with async_playwright() as p:
        guid = "88-73-84-53-00-00-08-E8"

        operations = [
            #"resetMeshInterface",
            #"meshInterfaceSelfDiagnosis",
            "testmessagertt4",
            #"testmessagertt2",
        ]

        # Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create output folder
        output_folder = os.path.join(
            os.getcwd(),
            f"Cirrus_OperationResults_{timestamp}"
        )
        os.makedirs(output_folder, exist_ok=True)

        # Report file inside the folder
        report_file = os.path.join(
            output_folder,
            "Cirrus_Execution_Report.txt"
        )

        # Open log file
        log_file = open(report_file, "w", encoding="utf-8")

        log_file.write("CIRRUS OPERATION EXECUTION REPORT\n")
        log_file.write("=" * 70 + "\n")
        log_file.write(f"Execution Start : {datetime.now()}\n\n")

        browser = await p.chromium.launch(
            channel="chrome",
            headless=True
        )

        context = await browser.new_context(
            storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
            ignore_https_errors=True
        )

        page = await context.new_page()
        try:
            await page.goto(
                ("https://10.41.177.62:8443/device/" +guid),
                wait_until="networkidle",
                timeout=60000
            )
        except Exception as e:
            print(f"❌ Unable to open device page: Application under maintanence/deployment")
            await browser.close()
            sys.exit(1)

        run_operation_btn = page.locator(
            "xpath=/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/button"
        )

        await expect(run_operation_btn).to_be_visible()
        await run_operation_btn.click()

        for operation_name in operations:

            print(f"\n==============================")
            print(f"Running {operation_name}")
            print(f"==============================")

            try:

                operation_input = page.locator("#name")
                await expect(operation_input).to_be_visible()
                await operation_input.clear()
                await operation_input.fill(operation_name)
                await page.wait_for_timeout(6000)
                await page.get_by_role(
                    "button",
                    name=operation_name
                ).click()
                await page.wait_for_timeout(6000)
                deploy_btn = page.get_by_role(
                    "button",
                    name="Deploy"
                )
                await expect(deploy_btn).to_be_enabled()
                await deploy_btn.click()
                await page.wait_for_timeout(30000)
                dialog = page.get_by_role("dialog")
                confirm_btn = dialog.get_by_role(
                    "button",
                    name="Deploy",
                    exact=True
                )
                await expect(confirm_btn).to_be_visible(timeout=10000)
                await confirm_btn.click()
                try:
                    close_btn = page.get_by_role(
                        "button",
                        name="Close"
                    )

                    if await close_btn.is_visible():
                        await close_btn.click()

                except Exception:
                    pass

                old_transaction = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
                )

                old_transaction_id = (
                    await old_transaction.text_content()
                ).strip()

                max_attempts = 11  # 11 x 60s = 11 minutes

                new_transaction_id = old_transaction_id

                for attempt in range(max_attempts):

                    print(
                        f"Waiting for transaction update "
                        f"({attempt + 1}/{max_attempts})..."
                    )

                    await page.wait_for_timeout(30000)

                    await page.reload(wait_until="networkidle")

                    latest_transaction = page.locator(
                        'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
                    )

                    new_transaction_id = (
                        await latest_transaction.text_content()
                    ).strip()

                    if new_transaction_id != old_transaction_id:
                        #print("✅ New transaction found")
                        break

                else:
                    raise Exception(
                        f"No new transaction generated after "
                        f"{max_attempts * 60} seconds"
                    )

                """
                old_timestamp_locator = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/p[1]'
                )
                
                old_timestamp = (
                    await old_timestamp_locator.text_content()
                ).strip()

                await page.wait_for_timeout(60000)

                await page.reload(wait_until="networkidle")
                """

                latest_transaction = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[2]'
                )

                await expect(latest_transaction).not_to_have_text(
                    old_transaction_id,
                    timeout=20000
                )

                new_transaction_id = (
                    await latest_transaction.text_content()
                ).strip()

                latest_timestamp_locator = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/p[1]'
                )

                new_timestamp = (
                    await latest_timestamp_locator.text_content()
                ).strip()

                latest_Transaction = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[1]/h6[1]'
                )

                latest_Transaction = (
                    await latest_Transaction.text_content()
                ).replace(" - response", "")

                latest_status = page.locator(
                    'xpath=//*[@id="root"]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/ul/li[1]/div[2]/div/span'
                )

                latest_status = (
                    await latest_status.text_content()
                ).strip()

                event_log_heading = page.get_by_text(
                    "Event Log - 7 Days",
                    exact=True
                )

                await event_log_heading.scroll_into_view_if_needed()

                box = await event_log_heading.bounding_box()

                screenshot_file = os.path.join(output_folder, f"{latest_Transaction}.png")
                """
                await page.screenshot(
                    path=screenshot_file,
                    clip={
                        "x": max(0, box["x"] - 20),
                        "y": max(0, box["y"] - 50),
                        "width": 1500,
                        "height": 550
                    }
                )
                """
                await page.screenshot(
                    path=screenshot_file,
                    full_page=True
                )
                print(f"GUID                : {guid}")
                print(f"Transaction Name    : {latest_Transaction}")
                print(f"Transaction ID      : {new_transaction_id}")
                print(f"Timestamp           : {new_timestamp}")
                print(f"Status              : {latest_status}")

                result = "PASSED" if latest_status == "SUCCESS" else "FAILED"
                output_text = (
                    "==============================\n"
                    f"Result - {operation_name}\n"
                    "==============================\n"
                    f"GUID             : {guid}\n"
                    f"Transaction Name : {latest_Transaction}\n"
                    f"Transaction ID   : {new_transaction_id}\n"
                    f"Timestamp        : {new_timestamp}\n"
                    f"Status           : {latest_status}\n"
                    f"Result           : {result}\n\n"
                )
                if latest_status == "SUCCESS":
                    print(f"✅ {operation_name} PASSED")
                else:
                    print(f"❌ {operation_name} FAILED")

                # Write to file
                log_file.write(output_text)
                log_file.flush()

                await page.get_by_text("View Payload", exact=True).first.click()

                dialog = page.get_by_role("dialog")
                await expect(dialog).to_be_visible()

                payload_text = await dialog.inner_text()

                payload_file = os.path.join(
                    output_folder,
                    f"{latest_Transaction}_payload.txt"
                )

                with open(payload_file, "w", encoding="utf-8") as f:
                    f.write(payload_text)
                    f.flush()

                print(f"✅ Payload saved")
                try:
                    await page.keyboard.press("Escape")
                except:
                    pass

                conn = psycopg2.connect(
                    host="10.0.117.69",
                    port="5432",
                    database="cirrusdb",
                    user="cirrusdevicetest",
                    password="cirrusdevicetestpass123"
                )

                print("Connected to PostgreSQL successfully")

                cursor = conn.cursor()

                cursor.execute("""
                SELECT *
                FROM cirrus.cirrus_operations
                WHERE "transactionId" = %s
                ORDER BY create_dt_ts DESC
                LIMIT 1
                """, (new_transaction_id,))

                row = cursor.fetchone()

                if row:

                    columns = [desc[0] for desc in cursor.description]

                    db_file = os.path.join(
                        output_folder,
                        f"{latest_Transaction}_DB_Output.txt"
                    )

                    with open(db_file, "w", encoding="utf-8") as db_output:

                        db_output.write("DATABASE OUTPUT\n")
                        db_output.write("=" * 80 + "\n\n")

                        for col, value in zip(columns, row):
                            db_output.write(f"{col}: {value}\n")

                    #print(f"✅ DB Output saved: {db_file}")


                await run_operation_btn.click()


            except Exception as e:
                print(f"❌ Error in {operation_name}: {e}")

        await browser.close()



if __name__ == "__main__":
    asyncio.run(main())