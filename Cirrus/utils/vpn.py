import requests

class VPNChecker:

    @staticmethod
    def validate():

        try:
            response = requests.get(
                "https://10.41.177.62:8443",
                verify=False,
                timeout=10
            )

            print(
                f"VPN Connected - {response.status_code}"
            )

            return True

        except Exception:

            print("VPN Not Connected")

            return False