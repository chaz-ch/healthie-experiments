from modules.healthie import Healthie

def main():

    H = Healthie("STAGE")
    
    try:
                
        variables = {
            "id": None
        }
        
        variables["id"] = '4108931' # type: ignore

        response = H.get_signup_url(variables)
        print(response)

        variables["id"] = '4053352' # type: ignore

        response = H.get_signup_url(variables)
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
