import pyautogui
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    context = browser.new_context(
        storage_state=r"C:\Users\chandrs4\PycharmProjects\WelcomeScreen\auth.json",
        ignore_https_errors=True
    )

    page = context.new_page()

    page.goto(
        "https://10.41.177.62:8443/device/88-73-84-54-00-02-D3-1A"
    )

    #page.wait_for_timeout(15000)

    pyautogui.hotkey("ctrl", "-")
    pyautogui.hotkey("ctrl", "-")
    pyautogui.hotkey("ctrl", "-")

    # Run Operation
    run_operation_btn = page.locator(
        "xpath=/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/button"
    )

    expect(run_operation_btn).to_be_visible()
    run_operation_btn.click()

    # Search operation
    operation_name = "testMessageRTT4"
    operation_input = page.locator("#name")

    expect(operation_input).to_be_visible()
    operation_input.fill(operation_name)

    page.get_by_text(
        operation_name,
        exact=True
    ).click()

    # Deploy
    deploy_btn = page.get_by_role(
        "button",
        name="Deploy"
    )

    expect(deploy_btn).to_be_enabled()
    deploy_btn.click()

    page.wait_for_timeout(3000)

    # Confirm Deployment
    confirm_btn = page.locator(
        "xpath=/html/body/div[8]/div/div/div/div[2]/div[2]/div[2]/button[1]"
    )

    expect(confirm_btn).to_be_visible()
    confirm_btn.click()

    # Close popup if present
    try:
        close_btn = page.get_by_role("button", name="Close")

        if close_btn.is_visible(timeout=5000):
            close_btn.click()

    except Exception:
        pass

    page.wait_for_timeout(15000)

    # Capture current first transaction before refresh
    old_transaction = page.locator("tbody tr").first.locator("td").nth(0).text_content()

    #print(f"Current Top Transaction: {old_transaction}")

    page.wait_for_timeout(60000)

    # Refresh
    try:
        refresh_btn = page.locator(
            "xpath=/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div[11]/div/div/div[1]/div[2]/button"
        )

        refresh_btn.click()
        #print("Refresh button pressed")

    except Exception:
        print("Refresh button not found")

    # Wait until a new transaction appears at the top
    expect(
        page.locator("tbody tr").first.locator("td").nth(0)).not_to_have_text(old_transaction,
        timeout=60000
    )

    print("✅ New transaction detected")

    # Get latest TestMessageRTT4 row
    latest_row = page.locator("tbody tr").first

    expect(latest_row).to_be_visible(timeout=60000)

    transaction_id = latest_row.locator("td").nth(0).text_content()
    timestamp = latest_row.locator("td").nth(1).text_content()
    task = latest_row.locator("td").nth(2).text_content()
    operation = latest_row.locator("td").nth(3).text_content()
    status = latest_row.locator("td").nth(4).text_content()

    print("\n===== Latest Transaction =====")
    print(f"Transaction ID : {transaction_id}")
    print(f"Timestamp      : {timestamp}")
    print(f"Task           : {task}")
    print(f"Operation      : {operation}")
    print(f"Status         : {status}")
    print("==============================")

    # Validations
    if status and status.strip().upper() == "SUCCESS":
        print(f"✅ Operation '{operation}' completed successfully")
    else:
        print(f"❌ Operation '{operation}' failed")
        print(f"Current Status: {status}")
