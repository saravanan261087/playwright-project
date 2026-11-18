import os
from datetime import datetime

import pytest

from config.testdata import GUID, OPERATIONS
from pages.cirruspage import CirrusPage

from utils.vpn import VPNChecker
from utils.report import ReportManager
from utils.screenshot import ScreenshotManager

from services.operationservice import OperationService
from services.transaction_service import TransactionService
from services.payload import PayloadService
from services.database import DatabaseService


@pytest.mark.asyncio
async def test_operations(page):

    assert VPNChecker.validate(), "VPN is not connected"

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_folder = os.path.join(
        "output",
        timestamp
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    report_path = os.path.join(
        output_folder,
        "Execution_Report.txt"
    )

    cirrus = CirrusPage(page)

    await cirrus.open_device(
        GUID
    )

    executor = OperationService(
        cirrus
    )

    transaction = TransactionService(
        page
    )

    passed_operations = []
    failed_operations = []

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report_file:

        for operation in OPERATIONS:

            try:

                print(
                    f"\nRunning Operation: {operation}"
                )

                # Open operation window every time
                await cirrus.open_operation_window()

                # Execute operation
                await executor.execute(
                    operation
                )

                # Wait for transaction
                await transaction.wait_for_new_transaction()

                # Get details
                details = await transaction.get_details()

                # Screenshot
                await ScreenshotManager.capture(
                    page,
                    output_folder,
                    details["name"]
                )

                # Save Payload
                await PayloadService.save_payload(
                    page,
                    output_folder,
                    details["name"]
                )

                # DB Validation
                columns, row = DatabaseService.get_transaction(
                    details["id"]
                )

                if row is None:

                    details["guid"] = GUID
                    details["status"] = "FAILED"
                    details["result"] = "FAILED"

                    failed_operations.append(
                        operation
                    )

                    ReportManager.write_result(
                        report_file,
                        operation,
                        details
                    )

                    continue

                # Save DB Output
                db_file = DatabaseService.save_transaction_output(
                    details["id"],
                    output_folder,
                    details["name"]
                )

                print(
                    f"DB Output saved: {db_file}"
                )

                details["guid"] = GUID

                details["result"] = (
                    "PASSED"
                    if details["status"] == "SUCCESS"
                    else "FAILED"
                )

                ReportManager.write_result(
                    report_file,
                    operation,
                    details
                )

                print(
                    f"Transaction ID : "
                    f"{details['id']}"
                )

                print(
                    f"Status : "
                    f"{details['status']}"
                )

                if details["status"] == "SUCCESS":

                    passed_operations.append(
                        operation
                    )

                else:

                    failed_operations.append(
                        operation
                    )

                    print(
                        f"Operation Failed "
                        f"(Ignored): {operation}"
                    )

            except Exception as e:

                print(
                    f"Exception while executing "
                    f"{operation}: {str(e)}"
                )

                failed_operations.append(
                    operation
                )

                try:

                    details = {
                        "guid": GUID,
                        "name": operation,
                        "id": "N/A",
                        "status": "FAILED",
                        "result": "FAILED"
                    }

                    ReportManager.write_result(
                        report_file,
                        operation,
                        details
                    )

                except Exception:
                    pass

        # ==================================================
        # FINAL EXECUTION SUMMARY
        # ==================================================

        total_count = len(OPERATIONS)
        passed_count = len(passed_operations)
        failed_count = len(failed_operations)

        report_file.write("\n\n")
        report_file.write("=" * 60 + "\n")
        report_file.write("EXECUTION SUMMARY\n")
        report_file.write("=" * 60 + "\n\n")

        report_file.write(
            f"Total Operations : {total_count}\n"
        )

        report_file.write(
            f"Passed Operations : {passed_count}\n"
        )

        report_file.write(
            f"Failed Operations : {failed_count}\n\n"
        )

        if failed_operations:

            report_file.write(
                "Failed Operation List\n"
            )

            report_file.write(
                "-" * 40 + "\n"
            )

            for operation in failed_operations:

                report_file.write(
                    f"{operation}\n"
                )

        report_file.write("\n")
        report_file.write("=" * 60 + "\n")

        report_file.flush()

    print(
        f"\nReport Generated : {report_path}"
    )