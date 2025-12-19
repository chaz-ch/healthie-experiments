import random
from modules.healthie import Healthie

CHAZ_AS_PATIENT = 4097532
CHAZ_AS_PROVIDER = 3996427


def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie("STAGE")

    try:
        # variables = {
        #     "id": str(CHAZ_AS_PATIENT)
        # }

        # response = H.get_ids(variables)

        variables = {
            "first_name": "Chaz",
            "last_name": "McTester",
            "email": f"chazlarson+{random.randint(1000000, 9999999)}@gmail.com",
            "dietitian_id": str(CHAZ_AS_PROVIDER),
            "skipped_email": False,
            "phone_number": "612-701-3658",
            "dont_send_welcome": False,
            "record_identifier": str(random.randint(1000000, 9999999)),
            "dob": "1962-04-08",
            "gender": "Male",
        }

        response = H.create_user(variables)
        print(response)

        # get their ID
        user_id = response["createClient"]["user"]["id"]

        if not user_id:
            print("User creation failed, no user_id returned.")
            return
        # create a conversation with them using my provider ID

        variables = {"id": str(user_id)}

        response = H.get_ids(variables)

        doc_share_id = response["user"]["doc_share_id"]

        response = H.get_signup_url(variables)
        print(response)

        signup_url = response["user"]["set_password_link"]
        print(signup_url)

        variables = {
            "simple_added_users": doc_share_id,
            "conversation_name": "created via API test",
            "owner_id": CHAZ_AS_PROVIDER,
            "initial_message": f"Hello, {user_id}, I am your navigator, {CHAZ_AS_PROVIDER}",
        }

        response = H.create_conversation(variables)
        print(response)

        conversation_id = response["createConversation"]["conversation"]["id"]

        variables = {
            "content": "This is a second test message",
            "conversation_id": conversation_id,
            "user_id": CHAZ_AS_PROVIDER,
            "org_chat": True,
            "hide_org_chat_confirmation": True,
        }

        response = H.create_note(variables)
        print(response)
        # add the standard welcome message to the conversation

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
