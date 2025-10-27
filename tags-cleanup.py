from modules.healthie import Healthie

def main():

    H = Healthie("STAGE")

    PROD_DELETES = {
        65198,
        67552,
        67821,
        67820
    }

    STAGE_DELETES = {
        31050,
        31051,
        31084,
        32130,
        32588,
        32522,
        33234,
        33233,
        33232,
        32488,
        32489,
        32295
    }

    STAGE_CREATES = {
        'status:created',
        'status:invited',
        'status:verified'
    }

    PROD_CREATES = {
        "Chart::ChartCreated",
        "Chart::OrderCreated",
        "Consent::TelemedicineSigned",
        "Engagement::Responsive",
        "Engagement::Unresponsive",
        "ReportType::MGP",
        "ReportType::MGPH",
        "ReportType::StandardMG",
        "Result::BAC::Absent",
        "Result::BAC::Present",
        "Result::BIRADS::0",
        "Result::BIRADS::1",
        "Result::BIRADS::2",
        "Result::BIRADS::3",
        "Result::BIRADS::4",
        "Result::BIRADS::5",
        "Result::BreastDensity::Dense",
        "Result::BreastDensity::NonDense",
        "Result::TCLifetimeRisk::Average",
        "Result::TCLifetimeRisk::High",
        "Result::TCLifetimeRisk::Intermediate",
        "Status::Accessed",
        "Status::Created",
        "Status::Invited"
    }
    try:

        response = H.list_tags()
        for tag in response['tags']:
            print(f"{tag['id']} {tag['name']}")


        for tag_id in STAGE_CREATES:
            response = H.create_tag({'name': tag_id})
            print(response)

        response = H.list_tags()
        for tag in response['tags']:
            print(f"{tag['id']} {tag['name']}")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
