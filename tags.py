from modules.healthie import Healthie
from modules.ids import get_report_type_tag_id, get_status_tag_id


def main():
    H = Healthie("STAGE")

    try:
        response = H.list_tags_with_users()
        print(response)

        sample_user_id = "4363493"
        # '31050'

        # inputs = {
        #     'name': generate_name()
        # }

        # response = H.create_tag(inputs)
        # print(response)

        # # {'createTag': {'tag': None, 'messages': [{'field': 'name', 'message': 'has already been taken'}]}}
        # new_tag_id = response['createTag']['tag']['id']
        # print (f"created tag id {new_tag_id}")

        BAD_TAG_MGH = "34379"  # report_type:MGH
        BAD_TAG_INVITED = "34313"  # status:invited

        # assign good invited tag
        response = H.assign_tag([get_status_tag_id("STAGE", "Created")], sample_user_id)
        print(response)

        # remove bad invited tag
        response = H.remove_tag(BAD_TAG_INVITED, sample_user_id)
        print(response)

        # assign good MGP tag
        response = H.assign_tag(
            [get_report_type_tag_id("STAGE", "MGP")], sample_user_id
        )
        print(response)

        # remove bad MGH tag
        response = H.remove_tag(BAD_TAG_MGH, sample_user_id)
        print(response)

        response = H.list_tags_with_users()
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
