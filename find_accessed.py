from modules.healthie import Healthie

PAGE_SIZE = (
    100  # The number of users to request per page (determine the server's limit)
)


def main():
    H = Healthie("PROD")

    all_users = []
    accessed_users = {}

    current_offset = 0

    # Loop until a page returns fewer results than the limit (PAGE_SIZE)
    while True:
        # Define the variables for the current query
        variables = {"offset": current_offset, "page_size": PAGE_SIZE}

        # print(f"Fetching users with offset: {current_offset}...")

        try:
            response = H.list_users_access(variables)

            users_on_page = response["users"]

            all_users.extend(users_on_page)
            print(
                f"Fetched {len(users_on_page)} users. Total so far: {len(all_users)} of which {len(accessed_users)} have accessed their account"
            )

            if not users_on_page:
                # No more users found, end the loop
                print("No more users to fetch. Loop complete.")
                break

            for user in users_on_page:
                if user["accessed_account"]:
                    accessed_users[user["id"]] = user["email"]

            # Check if this was the last page
            if len(users_on_page) < PAGE_SIZE:
                print("Last page retrieved. Loop complete.")
                break

            # Increment the offset for the next iteration
            current_offset += PAGE_SIZE

        except Exception as e:
            print(f"An error occurred during the API request: {e}")
            break

    print(f"{len(accessed_users)} have accessed their account:")

    for user in accessed_users:
        print(f"{user}: {accessed_users[user]}")


if __name__ == "__main__":
    main()
