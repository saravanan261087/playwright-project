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

    await cirrus.open_device(GUID)

    await cirrus.open_operation_window()

    executor = OperationService(cirrus)

    transaction = TransactionService(page)

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report_file:

        for operation in OPERATIONS:

            print(
                f"\nRunning Operation: {operation}"
            )

            await executor.execute(
                operation
            )

            await transaction.wait_for_new_transaction()

            details = await transaction.get_details()

            # Screenshot
            await ScreenshotManager.capture(
                page,
                output_folder,
                details["name"]
            )

            # Payload Save
            await PayloadService.save_payload(
                page,
                output_folder,
                details["name"]
            )

            # DB Validation
            columns, row = DatabaseService.get_transaction(
                details["id"]
            )

            assert row is not None, (
                f"No database record found for "
                f"{details['id']}"
            )

            # Save DB Output File
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

            assert details["status"] == "SUCCESS", (
                f"Operation {operation} failed. "
                f"Transaction ID: {details['id']}"
            )