BASE_URL = "https://10.41.177.62:8443"

AUTH_FILE = r"auth/auth.json"

DB_CONFIG = {
    "host": "10.0.117.69",
    "port": "5432",
    "database": "cirrusdb",
    "user": "cirrusdevicetest",
    "password": "cirrusdevicetestpass123"
}

HEADLESS = True

TRANSACTION_WAIT_ATTEMPTS = 11
TRANSACTION_WAIT_SECONDS = 30