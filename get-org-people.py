from modules.healthie import Healthie

def main():

    H = Healthie("PROD")

    try:

        variables = {
            'keywords': None,
            'offset': None,
            'page_size': 50
        }

        response = H.get_org_users(variables)
        for member in response['organizationMembers']:
            if member['is_active_provider']:
                print(f"{member['id']} {member['full_name']:<20} {member['email']}")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
