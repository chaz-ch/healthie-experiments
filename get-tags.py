from modules.healthie import Healthie

def main():

    H = Healthie("STAGE")

    try:

        response = H.list_tags_with_users()
        for tag in response['tags']:
            print(f"{tag['id']} {tag['name']}  -  {len(tag['tagged_users'])} users")
            for user in tag['tagged_users']:
                print(f" - {user['id']} {user['name']}")

        response = H.list_tags()
        for tag in response['tags']:
            print(f"{tag['id']} {tag['name']}")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
