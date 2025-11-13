from modules.healthie import Healthie

updated_ids = [
    10666933,
    10578403,
    10578423,
    10410358,
    10578357,
    11008105,
    11008180,
]


def main():
    H = Healthie("PROD")

    access_count = 0
    total_count = 0
    incomplete_count = 0
    reactivate_count = 0
    signup_completed_count = 0
    have_last_sign_in_count = 0

    for hid in updated_ids:
        try:
            total_count = total_count + 1

            variables = {"id": hid}

            response = H.get_user_details(variables)
            print(f"{total_count}  {response}")

            if response["user"]["last_sign_in_at"]:
                have_last_sign_in_count += 1

            if response["user"]["accessed_account"]:
                access_count += 1

            if response["user"]["any_incomplete_onboarding_steps"]:
                incomplete_count += 1

            if response["user"]["requires_reactivation"]:
                reactivate_count += 1

            if response["user"]["signup_completed"]:
                signup_completed_count += 1

        except Exception as e:
            print(f"An error occurred: {e}")

    print(
        f"Total: {total_count}, Have a Last Sign In: {have_last_sign_in_count}, Accessed: {access_count}, Incomplete: {incomplete_count}, Reactivate: {reactivate_count}, Signup Completed: {signup_completed_count}"
    )


if __name__ == "__main__":
    main()
