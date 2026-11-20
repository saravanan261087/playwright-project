from playwright.sync_api import sync_playwright


def test_users_api():
    with sync_playwright() as p:

        request = p.request.new_context(
            ignore_https_errors=True
        )

        response = request.get(
            "https://jsonplaceholder.typicode.com/users"
        )

        print("Status Code:", response.status)

        assert response.status == 200

        users = response.json()

        print("Number of Users:", len(users))

        for user in users:
            print(user["name"])


if __name__ == "__main__":
    test_users_api()