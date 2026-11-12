from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    context = browser.new_context(
        ignore_https_errors=True
    )

    page = context.new_page()

    page.goto("https://10.41.177.62:8443")

    input("Login manually and press Enter after successful login...")

    context.storage_state(path="auth.json")

    print("auth.json created successfully")

    browser.close()
