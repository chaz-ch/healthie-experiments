import csv
import datetime
from modules.healthie import Healthie
from modules.util import (
    convert_date_format,
    standardize_gender,
    is_valid_email,
    validate_phone_number,
)
from modules.ids import (
    get_bac_tag_id,
    get_birad_tag_id,
    get_alr_tag_id,
    get_breast_density_tag_id,
    get_report_type_tag_id,
    get_status_tag_id,
    get_global_provider_id,
    get_smi_inbound_group_id,
)

# Path to your CSV file
CSV_FILE_PATH = "healthie-hx-load-1027-a.csv"

# TARGET_ENV = "STAGE"
TARGET_ENV = "PROD"


def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie(TARGET_ENV)
    rt_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = open(f"user_actions-{TARGET_ENV}-{rt_str}.txt", "a")
    responses = open(f"api_responses-{TARGET_ENV}-{rt_str}.txt", "a")

    print("Action\tHealthie ID\tCascaid ID", file=log)

    created_count = 0
    updated_count = 0
    error_count = 0
    row_index = 0
    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # batch_published_dt,
            # status,
            # navigator_name,
            # navigation_consent_flag,
            # terms_and_privacy_policy_flag,
            # telemedicine_consent_flag,
            # membership_agreement_flag,
            # userid,                        <=====
            # firstname,                     <=====
            # lastname,                      <=====
            # dateofbirth,                   <=====
            # gender,                        <=====
            # birad,                         <=====
            # lifetimerisk,
            # lifetimerisknbr,               <=====
            # breastdensity,                 <=====
            # email,                         <=====
            # phonenumber,                   <=====
            # bac,                           <=====
            # reporttype,                    <=====
            # referring_provider_first_nm,   <=====
            # referring_provider_last_nm,    <=====
            # referring_provider_npi_nbr,    <=====
            # referral_reason                <=====
            for row in csv_reader:
                row_index += 1
                print(f"Processing row: {row_index}")
                print(
                    f"created: {created_count}, updated: {updated_count}, errors: {error_count}"
                )

                # Must have - Phase 1:
                #     Patient First name                       √
                #     Patient Last Name                        √
                #     Patient Email Address                    √
                #     Patient Phone Number                     √
                #     Patient Date of Birth                    √
                #     Patient Sex at Birth                     √
                #     Navigator Name [Helathie ID of Provider] √
                print(row, file=responses)

                user_id = row.get("userid")
                user_email = row.get("email")
                user_first_name = str(row.get("firstname")).title()
                user_last_name = str(row.get("lastname")).title()
                user_dob = convert_date_format(row.get("dateofbirth"))
                user_gender = standardize_gender(row.get("gender"))
                user_phone_number = validate_phone_number(row.get("phonenumber"))
                user_birad = row.get("birad")
                user_lifetimerisknbr = (
                    float(str(row.get("lifetimerisknbr")))
                    if row.get("lifetimerisknbr")
                    else None
                )
                user_breastdensity = row.get("breastdensity")
                user_bac = row.get("bac")
                user_reporttype = row.get("reporttype")
                user_referring_provider_first_nm = str(
                    row.get("referring_provider_first_nm")
                ).title()
                user_referring_provider_last_nm = str(
                    row.get("referring_provider_last_nm")
                ).title()
                user_referring_provider_npi_nbr = row.get("referring_provider_npi_nbr")
                user_referral_reason = str(row.get("referral_reason"))

                # get_welcome_email = row.get("navigation_consent_flag") == "Y"
                # no_welcome_email = not get_welcome_email

                # Nobody gets an email for the historical load
                no_welcome_email = True

                variables = {
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "email": user_email,
                    "dietitian_id": get_global_provider_id(TARGET_ENV),
                    "skipped_email": not is_valid_email(user_email),
                    "phone_number": user_phone_number,
                    "dont_send_welcome": no_welcome_email,
                    "record_identifier": user_id,
                    "dob": user_dob,
                    "gender": user_gender,
                    "user_group_id": get_smi_inbound_group_id(TARGET_ENV),
                }

                print(variables, file=responses)

                response = H.create_user(variables)
                print(response, file=responses)

                new_user_id = None
                action = "created"

                if response["createClient"]["user"]:
                    # {'createClient': {'user': {'id': '4181385'}, 'messages': None}}
                    new_user_id = response["createClient"]["user"]["id"]
                    print(f"Created user id {new_user_id}")
                    created_count += 1
                else:
                    # {'createClient': {'user': None, 'messages': [{'field': 'email', 'message': 'The email address that you entered already exists for your client Test McTest.'}]}}
                    if response["createClient"]["messages"]:
                        if (
                            "The email address that you entered already exists"
                            in response["createClient"]["messages"][0]["message"]
                        ):
                            # This person already exists in healthie
                            print(
                                "This person already exists in healthie, let's find them:"
                            )

                            response = H.get_user_by_email(str(user_email))
                            print(response, file=responses)

                            if len(response["users"]) > 0:
                                new_user_id = response["users"][0]["id"]
                                # now we need to update the user with the other information
                                variables["id"] = new_user_id
                                variables.pop(
                                    "dietitian_id"
                                )  # ERROR: "Clients cannot get assigned to a support member"
                                variables["dont_send_welcome"] = (
                                    True  # if they already have an account, we don't want to send them a welcome email
                                )

                                response = H.update_user(variables)
                                print(response, file=responses)

                                print(f"Updated user id {new_user_id}")
                                action = "updated"
                                updated_count += 1
                            else:
                                print("No user found, even though creation failed")
                                print("exiting")
                                error_count += 1
                                exit()

                        else:
                            print(response)
                            print("exiting")
                            error_count += 1
                            exit()

                print(f"{action}\t{new_user_id}\t{user_id}", file=log)

                if new_user_id:
                    # Tags - Phase 1:
                    #     Tags -
                    #     1) Status: Created (Phase 1)
                    #     2) Patient Report Type (Phase 1)
                    #         MGP - Mammogram+
                    #         MGPH - Mammogram + Heart

                    # As shown here:
                    #     <https://cascaidhealth.atlassian.net/wiki/spaces/SRN/pages/140705795/Healthie+Tags>
                    # these tags have been created in Healthie:
                    # 'Status::Created':                      '32355'
                    # 'ReportType::MGP':                      '32338'
                    # 'ReportType::MGPH':                     '32339'

                    if user_reporttype:
                        REPORT_TYPE_TAG = get_report_type_tag_id(
                            TARGET_ENV, user_reporttype
                        )

                        print(f"{user_reporttype}: {REPORT_TYPE_TAG}")

                        # assign tags to that new user:
                        response = H.assign_tag(
                            [get_status_tag_id(TARGET_ENV, "Created"), REPORT_TYPE_TAG],
                            new_user_id,
                        )
                        print(response, file=responses)

                    # Nice to have Phase 1:
                    #     Patient Medical Data (As tags)
                    #          (Nice to have Phase 1)
                    #                 Patient Breast Density
                    #                     Only one value would be sent
                    #                     Potential Values: A, B, C, D
                    # 'Result::BreastDensity::Dense':         '32349'
                    # 'Result::BreastDensity::NonDense':      '32350'

                    if user_breastdensity:
                        try:
                            BREAST_DENSITY_TAG = get_breast_density_tag_id(
                                TARGET_ENV, user_breastdensity
                            )
                        except Exception:
                            BREAST_DENSITY_TAG = None

                        print(f"{user_breastdensity}: {BREAST_DENSITY_TAG}")

                        if BREAST_DENSITY_TAG:
                            response = H.assign_tag([BREAST_DENSITY_TAG], new_user_id)
                            print(response, file=responses)
                        else:
                            print("No breast density tag to assign")

                    #                 Patient Lifetime Risk
                    #                     Only one value would be sent
                    #                     Potential Values: Average, Intermediate, High
                    # 'Result::TCLifetimeRisk::Average':      '32351'
                    # 'Result::TCLifetimeRisk::High':         '32352'
                    # 'Result::TCLifetimeRisk::Intermediate': '32353'

                    if user_lifetimerisknbr:
                        LIFETIME_RISK_TAG = get_alr_tag_id(
                            TARGET_ENV, user_lifetimerisknbr
                        )

                        print(f"{user_lifetimerisknbr}: {LIFETIME_RISK_TAG}")

                        response = H.assign_tag([LIFETIME_RISK_TAG], new_user_id)
                        print(response, file=responses)

                    if user_birad:
                        BIRAD_TAG = get_birad_tag_id(TARGET_ENV, user_birad)

                        print(f"{user_birad}: {BIRAD_TAG}")

                        if BIRAD_TAG:
                            response = H.assign_tag([BIRAD_TAG], new_user_id)
                            print(response, file=responses)
                        else:
                            print("No BIRAD tag to assign")

                    if user_bac:
                        BAC_TAG = get_bac_tag_id(TARGET_ENV, user_bac)

                        print(f"{user_bac}: {BAC_TAG}")

                        if BAC_TAG:
                            response = H.assign_tag([BAC_TAG], new_user_id)
                            print(response, file=responses)
                        else:
                            print("No BAC tag to assign")

                    if (
                        user_referring_provider_npi_nbr
                        and user_referring_provider_first_nm
                        and user_referring_provider_last_nm
                    ):
                        variables = {
                            "input": {
                                "first_name": user_referring_provider_first_nm,
                                "last_name": user_referring_provider_last_nm,
                                "npi": user_referring_provider_npi_nbr,
                            }
                        }

                        print(variables, file=responses)

                        response = H.create_referring_physician(variables)
                        print(response, file=responses)
                        # {'createReferringPhysician': {'duplicated_physician': None, 'messages': None, 'referring_physician': {'id': '42306', 'full_name': 'admiring_chaum competent_knuth', 'npi': '5654222254'}}}
                        try:
                            if response["createReferringPhysician"][
                                "duplicated_physician"
                            ]:
                                physician_id = response["createReferringPhysician"][
                                    "duplicated_physician"
                                ]["id"]
                            elif response["createReferringPhysician"][
                                "referring_physician"
                            ]:
                                physician_id = response["createReferringPhysician"][
                                    "referring_physician"
                                ]["id"]
                            else:
                                exit()
                        except Exception as e:
                            print(f"{e}")
                            exit()

                        # reason not required
                        variables = {
                            "input": {
                                "referral_reason": user_referral_reason,
                                "referring_physician_id": physician_id,
                                "user_id": new_user_id,
                            }
                        }

                        print(variables, file=responses)

                        response = H.create_referral(variables)
                        print(response, file=responses)
                        # {"data": {"createReferral": {"messages": null,"referral": {"id": "57421"}}}}

                        try:
                            referral_id = response["createReferral"]["referral"]["id"]
                        except Exception as e:
                            print(f"{e}")
                            exit()

            print("Final tally")
            print(
                f"created: {created_count}, updated: {updated_count}, errors: {error_count}"
            )

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "log" in locals() and not log.closed:
            log.close()
            print("log closed.")


if __name__ == "__main__":
    main()
