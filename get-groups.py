from modules.healthie import Healthie

def main():

    H = Healthie("STAGE")

    try:

        response = H.list_groups()
        print(f"{response['userGroupsCount']} groups found")
        for tag in response['userGroups']:
            print(f"{tag['id']} {tag['name']} {tag['users_count']}")

        response = H.list_groups_with_users()
        print(f"{response['userGroupsCount']} groups found")
        for tag in response['userGroups']:
            print(f"{tag['id']} {tag['name']} {tag['users_count']}")
            for user in tag['users']:
                print(f"    {user['id']} {user['name']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
