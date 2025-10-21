from modules.healthie import Healthie


CHAZ_AS_PATIENT = 4097532
CHAZ_AS_PROVIDER = 3996427

def main():

    H = Healthie("STAGE")
    
    try:
                
        variables = {
            "id": None
        }
        
        variables["id"] = str(CHAZ_AS_PATIENT)

        response = H.get_ids(variables)
        print(response)

        variables["id"] = str(CHAZ_AS_PROVIDER)

        response = H.get_ids(variables)
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
