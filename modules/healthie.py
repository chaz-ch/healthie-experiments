import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()


class Healthie:
    """
    A client class for managing authenticated connections and operations
    to Healthie.
    """

    def __init__(self, environment: str):
        """
        Initializes the secure GraphQL client with authentication.
        """
        if not environment:
            environment = "STAGE"
        else:
            environment = environment.upper()

        THE_URL = os.getenv(f"HEALTHIE_{environment}_URL")
        THE_API_KEY = os.getenv(f"HEALTHIE_{environment}_API_KEY")

        if not THE_URL:
            raise ValueError(f"No HEALTHIE_{environment}_URL in the environment.")
        if not THE_API_KEY:
            raise ValueError(f"No HEALTHIE_{environment}_API_KEY in the environment.")

        self.endpoint = str(os.getenv(f"HEALTHIE_{environment}_URL"))
        self.api_key = os.getenv(f"HEALTHIE_{environment}_API_KEY")

        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "AuthorizationSource": "API",
        }

    def _execute_request(
        self, query: str, variables: Optional[Dict[str, Any]] = None, timeout: int = 10
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"query": query}
        if variables is not None:
            payload["variables"] = variables

        try:
            response = requests.post(
                self.endpoint, json=payload, headers=self.headers, timeout=timeout
            )
            response.raise_for_status()

            data: Dict[str, Any] = response.json()

            if "errors" in data:
                error_messages: List[str] = [
                    err.get("message", "Unknown GraphQL Error")
                    for err in data["errors"]
                ]
                raise ValueError(f"GraphQL Query Error(s): {'; '.join(error_messages)}")

            return data

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"API Request Error: {e}")

    def _execute_upload_request(
        self, input_data: Dict[str, Any], files: Dict[str, Any], timeout: int = 10
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                str(self.endpoint),
                data=input_data,
                files=files,
                headers=self.headers,
                timeout=timeout,
            )

            response.raise_for_status()

            data: Dict[str, Any] = response.json()

            if "errors" in data:
                error_messages: List[str] = [
                    err.get("message", "Unknown GraphQL Error")
                    for err in data["errors"]
                ]
                raise ValueError(f"GraphQL Query Error(s): {'; '.join(error_messages)}")

            return data

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"API Request Error: {e}")

    # user-related

    def create_user(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
    mutation createClient(
    $first_name: String!
    $last_name: String!
    $email: String!
    $dietitian_id: String!
    $skipped_email: Boolean
    $phone_number: String
    $dont_send_welcome: Boolean
    $record_identifier: String
    $dob: String
    $gender: String
    $additional_record_identifier: String
    $legal_name: String
    $metadata: String
    $other_provider_ids: [String]
    $restricted: Boolean
    $skip_set_password_state: Boolean
    $timezone: String
    $user_group_id: String
) {
    createClient(
        input: {
        first_name: $first_name
        last_name: $last_name
        email: $email
        skipped_email: $skipped_email
        phone_number: $phone_number
        dont_send_welcome: $dont_send_welcome
        record_identifier: $record_identifier
        dob: $dob
        gender: $gender
        dietitian_id: $dietitian_id
        additional_record_identifier: $additional_record_identifier
        legal_name: $legal_name
        metadata: $metadata
        other_provider_ids: $other_provider_ids
        restricted: $restricted
        skip_set_password_state: $skip_set_password_state
        timezone: $timezone
        user_group_id: $user_group_id
        }
    ) {
        user {
        id
        }
        messages {
        field
        message
        }
    }
    }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def update_user(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        mutation updateClient(
            $id: ID!,
            $first_name: String,
            $last_name: String,
            $legal_name: String,
            $email: String,
            $active: Boolean,
            $additional_phone_number: String,
            $additional_record_identifier: String,
            $current_email: String,
            $dietitian_id: String,
            $dob: String,
            $gender: String,
            $phone_number: String,
            $resend_welcome: Boolean,
            $send_form_request_reminder: Boolean,
            $skipped_email: Boolean,
            $timezone: String,
            $user_group_id: String) {
        updateClient(
            input: {
                id: $id,
                first_name: $first_name,
                last_name: $last_name,
                legal_name: $legal_name,
                email: $email
                active: $active,
                additional_phone_number: $additional_phone_number,
                additional_record_identifier: $additional_record_identifier,
                current_email: $current_email,
                dietitian_id: $dietitian_id,
                dob: $dob,
                gender: $gender,
                phone_number: $phone_number,
                resend_welcome: $resend_welcome,
                send_form_request_reminder: $send_form_request_reminder,
                skipped_email: $skipped_email,
                timezone: $timezone,
                user_group_id: $user_group_id
            }
        ) {
            user {
                id
                first_name
                last_name
                legal_name
                email,
                active,
                additional_phone_number,
                additional_record_identifier,
                dietitian_id,
                dob,
                gender,
                phone_number,
                skipped_email,
                timezone,
                user_group_id
            }
            messages {
                field
                message
            }
        }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def update_user_record_identifier(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        mutation updateClient(
            $id: ID!,
            $record_identifier: String,
            $additional_record_identifier: String) {
        updateClient(
            input: {
                id: $id,
                record_identifier: $record_identifier,
                additional_record_identifier: $additional_record_identifier
            }
        ) {
            user {
                id
                record_identifier
                additional_record_identifier
            }
            messages {
                field
                message
            }
        }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_users(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
query users(
    $offset: Int
    $keywords: String
    $sort_by: String
    $active_status: String
    $group_id: String
    $show_all_by_default: Boolean
    $should_paginate: Boolean
    $provider_id: String
    $conversation_id: ID
    $limited_to_provider: Boolean
) {
    usersCount(
    keywords: $keywords
    active_status: $active_status
    group_id: $group_id
    conversation_id: $conversation_id
    provider_id: $provider_id
    limited_to_provider: $limited_to_provider
    )
    users(
    offset: $offset
    keywords: $keywords
    sort_by: $sort_by
    active_status: $active_status
    group_id: $group_id
    conversation_id: $conversation_id
    show_all_by_default: $show_all_by_default
    should_paginate: $should_paginate
    provider_id: $provider_id
    limited_to_provider: $limited_to_provider
    ) {
    id
    }
}
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_users_access(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
query users(
    $offset: Int
    $page_size: Int
) {
    users(
    offset: $offset
    page_size: $page_size
    ) {
    id
    email
    accessed_account
    }
}        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_users_completed_intake(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
query users(
    $offset: Int
    $page_size: Int
) {
    users(
    offset: $offset
    page_size: $page_size
    ) {
    id
    email
    has_completed_intake_forms
    }
}        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def get_signup_url(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        query getUser($id: ID) {
        user(id: $id) {
            id
            name
            email
            phone_number
            set_password_link
        }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def get_user_details(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        query getUser($id: ID) {
            user(id: $id) {
                id
                name
                email
                phone_number
                accessed_account
                any_incomplete_onboarding_steps
                created_at
                last_active
                last_activity
                last_sign_in_at
                requires_reactivation
                signup_completed
            }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def get_sent_notification_records(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        query getUser($id: ID) {
            user(id: $id) {
                id
                name
                email
                phone_number
                accessed_account
                any_incomplete_onboarding_steps
                created_at
                last_active
                last_activity
                last_sign_in_at
                requires_reactivation
                signup_completed
            }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def get_ids(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        query getUser($id: ID) {
        user(id: $id) {
            id
            name
            doc_share_id
            record_identifier
            additional_record_identifier
            }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def find_users_by_keywords(self, keywords) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param keywords: The comma-separated string of keywords to search for.
        """

        input_data = {"keywords": keywords}

        mutation = """
        query users($keywords: String) {
            users(keywords: $keywords) {
                id
            }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        return self.find_users_by_keywords(email)

    def get_org_users(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to modify a new resource.

        :param keywords: The comma-separated string of keywords to search for.
        """

        mutation = """
query organizationMembers(
  $keywords: String
  $offset: Int
  $page_size: Int
) {
  organizationMembers(
    keywords: $keywords
    offset: $offset
    page_size: $page_size
  ) {
    id
    full_name
    email
    active
    is_active_provider
  }
}
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # tag-related

    def create_tag(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        mutation = """
        mutation createTag($name: String, $taggable_user_id: ID) {
        createTag(input: { name: $name, taggable_user_id: $taggable_user_id }) {
            tag {
            id
            name
            tagged_users {
                id
            }
            }

            messages {
                field
                message
            }
            }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def assign_tag(self, tag_ids: list[str], user_id: str) -> Dict[str, Any]:
        mutation = """
        mutation applyTags($ids: [ID], $taggable_user_id: ID) {
            bulkApply(input: { ids: $ids, taggable_user_id: $taggable_user_id }) {
            tags {
                id
                name
            }

            messages {
                field
                message
            }
            }
        }
        """
        inputs = {"ids": tag_ids, "taggable_user_id": user_id}

        try:
            response = self._execute_request(mutation, inputs)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def remove_tag(self, tag_id: str, user_id: str) -> Dict[str, Any]:
        mutation = """
        mutation removeAppliedTag($id: ID, $taggable_user_id: ID) {
            removeAppliedTag(input: { id: $id, taggable_user_id: $taggable_user_id }) {
            tag {
                id
                name
            }

            messages {
                field
                message
            }
            }
        }
        """
        inputs = {"id": tag_id, "taggable_user_id": user_id}

        try:
            response = self._execute_request(mutation, inputs)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_tags(self) -> Dict[str, Any]:
        query = """
        query tags {
            tags {
            id
            name
            }
        }
        """
        try:
            response = self._execute_request(query)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_tags_with_users(self) -> Dict[str, Any]:
        query = """
        query tags {
            tags {
            id
            name
            tagged_users {
                name
                id
            }
            }
        }
        """
        try:
            response = self._execute_request(query)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def delete_tag(self, tag_id: str) -> Dict[str, Any]:
        mutation = """
        mutation deleteTag($id: ID) {
            deleteTag(input: { id: $id }) {
            tag {
                id
                name
            }

            messages {
                field
                message
            }
            }
        }
        """
        inputs = {"id": tag_id}

        try:
            response = self._execute_request(mutation, inputs)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # document-related

    def create_document(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        if variables["display_name"] is None:
            temp_file = Path(variables["file_path"])
            variables["display_name"] = temp_file.stem

        file = open(variables["file_path"], "rb")

        inputs = {
            "file:": None,  # Upload
            "rel_user_id": variables["rel_user_id"],
            "share_with_rel": variables["share_with_rel"],
            "display_name:": variables["display_name"],
            "clients_ids:": variables["clients_ids"],
            "provider_ids:": variables["provider_ids"],
        }

        mutation = """
        mutation createDocument(
            $file: Upload,
            $rel_user_id: String,
            $share_with_rel: Boolean,
            $display_name: String,
            $clients_ids: String,
            $provider_ids: [String],

            ) {
            createDocument(input: {
            file: $file,
            rel_user_id: $rel_user_id,
            share_with_rel: $share_with_rel,
            display_name: $display_name,
            clients_ids: $clients_ids,
            provider_ids: $provider_ids,
            }) {
            document {
                id
            }
            messages {
                field
                message
            }
            }
        }
        """

        operations = json.dumps({"query": mutation, "variables": inputs})

        map = json.dumps({"0": ["variables.file"]})

        data = {"operations": operations, "map": map}

        files = {"0": file}

        response = self._execute_upload_request(data, files)

        return response.get("data", {})

    def list_documents(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        inputs = variables

        mutation = """
        query documents(
            $offset: Int
            $keywords: String
            $folder_id: String
            $file_types: [String]
            $file_type: String
            $sort_by: String
            $private_user_id: String
            $viewable_user_id: String
            $consolidated_user_id: String
            $filter: String
            $should_paginate: Boolean
            $for_template_use: Boolean
            $provider_id: ID
        ) {
            documents(
                offset: $offset
                keywords: $keywords
                folder_id: $folder_id
                file_types: $file_types
                file_type: $file_type
                sort_by: $sort_by
                private_user_id: $private_user_id
                viewable_user_id: $viewable_user_id
                consolidated_user_id: $consolidated_user_id
                filter: $filter
                should_paginate: $should_paginate
                for_template_use: $for_template_use
                provider_id: $provider_id
            ) {
                id
                display_name
                file_content_type
                opens {
                    id
                }
                owner {
                    id
                    email
                }
                users {
                    id
                    email
                }
            }
        }
        """

        response = self._execute_request(mutation, inputs)

        return response.get("data", {})

    # Conversation [chat] related

    def create_conversation(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        mutation = """
            mutation createConversation(
            $input: createConversationInput
            ) {
            createConversation(input: $input) {
                conversation {
                    id
                    invitees {
                        id
                    }
                    name
                    owner {
                        id
                    }
                    updated_at
                }
            }
            }
        """

        createConversationInput = {
            "name": variables["conversation_name"],
            "owner_id": variables["owner_id"],
            "note": {"content": variables["initial_message"]},
            "simple_added_users": variables["simple_added_users"],
        }

        inputs = {"input": createConversationInput}
        try:
            response = self._execute_request(mutation, inputs)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def create_note(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        createNoteInput = {
            "input": {
                "content": variables["content"],
                "conversation_id": variables["conversation_id"],
                "user_id": variables["conversation_id"],
                "org_chat": variables["org_chat"],
                "hide_org_chat_confirmation": variables["hide_org_chat_confirmation"],
            }
        }

        # createNoteInput
        # {
        #     attached_audio: Upload
        #     attached_document: Upload
        #     attached_image: Upload
        #     attached_image_string: String
        #     content: String
        #     conversation_id: String
        #     created_at: String
        #     hide_org_chat_confirmation: Boolean
        #
        #     """
        #     True, if a note create action called in the organization chat context
        #     """
        #     org_chat: Boolean
        #     scheduled_at: String
        #     updated_at: String
        #     user_id: String
        # }

        mutation = """
        mutation createNote($input: createNoteInput) {
            createNote(input: $input) {
                messages {
                    field
                    message
                }
                note {
                    id
                }
            }
        }
        """

        try:
            response = self._execute_request(mutation, createNoteInput)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_conversationMemberships(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        inputs = variables

        mutation = """
query conversationMemberships(
  $org_chat: Boolean
  $provider_id: ID
  $offset: Int
  $page_size: Int
) {
  conversationMemberships(
    org_chat: $org_chat
    provider_id: $provider_id
    offset: $offset
    page_size: $page_size
  ) {
    conversation_id
    display_name
    convo {
      id
      patient_id
      last_note_viewed_id
    }
  }
}"""

        response = self._execute_request(mutation, inputs)

        return response.get("data", {})

    def get_notes(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        inputs = variables

        mutation = """
query notes(
  $conversation_id: ID
  $offset: Int
  $page_size: Int
) {
  notes(
    conversation_id: $conversation_id
    offset: $offset
    page_size: $page_size
  ) {
    created_at
    creator { id }
    content
    id
    is_autoresponse
    user_id
    viewed
  }
}"""

        response = self._execute_request(mutation, inputs)

        return response.get("data", {})

    # task-related

    def create_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """
        # assignee_ids · [ID!] · IDs of the users assigned to this task
        # client_id · String · The identifier of the client (patient) associated with this task
        # complete · Boolean Optional. Set to true if the Task is already complete
        # completed_by_id · ID
        # $content: String 	Content of the Task
        # created_by_id · String · The ID of the user (provider or staff member) who is listed as creating the task
        # $due_date: String Optional. A due date of the Task
        # note_id · ID
        # $priority: Int 0 or 1
        # $reminder: TaskReminderInput
        #   reminder.is_enabled	Set to true to enable the reminder, false otherwise
        #   reminder.reminder_time	Time, expressed in number of minutes from midnight, to trigger the reminder at
        #   reminder.interval_type	Frequency of the reminder. Possible options are:
        #     daily
        #     weekly
        #     once - default
        #   reminder.interval_value	Date when to trigger the reminder
        # seen · Boolean

        mutation = """
        mutation createTask(
            $assignee_ids: [ID!]
            $client_id: String
            $complete: Boolean
            $completed_by_id: ID
            $content: String
            $due_date: String
            $note_id: ID
            $priority: Int
            $reminder: TaskReminderInput
        ) {
        createTask(
            input: {
            assignee_ids: $assignee_ids
            client_id: $client_id
            complete: $complete
            completed_by_id: $completed_by_id
            content: $content
            due_date: $due_date
            note_id: $note_id
            priority: $priority
            reminder: $reminder
            }
        ) {
            task {
            id
            }
            messages {
            field
            message
            }
        }
        }
        """

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Referral-related

    def create_referring_physician(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        mutation = """
mutation createReferringPhysician($input: createReferringPhysicianInput) {
  createReferringPhysician(input: $input) {
    duplicated_physician {
      id
    }
    messages {
      field
      message
    }
    referring_physician {
      id
      full_name
      npi
    }
  }
}
"""

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def create_referral(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        mutation = """
mutation createReferral($input: createReferralInput) {
  createReferral(input: $input) {
    messages {
      field
      message
    }
    referral {
      id
    }
  }
}
"""

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Forms

    def create_filled_form(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource.

        :param input_data: The dictionary of data to pass as the input variable.
        """

        mutation = """
        mutation createFormAnswerGroup(
            # Should almost always true
            $finished: Boolean
            # ID of the custom_module_form (e.g "100")
            $custom_module_form_id: String
            # ID of the patient (e.g "61")
            $user_id: String
            # e.g [{custom_module_id: "1", answer: "foo", user_id: "61"}, {custom_module_id: "2", answer: "bar", user_id: "61"}]
            $form_answers: [FormAnswerInput!]!
        ) {
        createFormAnswerGroup(
            input: {
            finished: $finished
            custom_module_form_id: $custom_module_form_id
            user_id: $user_id
            form_answers: $form_answers
            }
        ) {
            form_answer_group {
            id
            }
            messages {
            field
            message
            }
        }
        }
        """

        # created_at · String! · required · The date on which the template was created
        # cursor · Cursor! · required · Pagination cursor
        # custom_modules · [CustomModule!]! · required · The questions in the template
        # external_id · String · Custom column used by API users. Used to relate our form objects with objects in third-party systems
        # external_id_type · String · Custom column used by API users. Used to relate our form objects with objects in third-party systems
        # form_answer_groups · [FormAnswerGroup!]! · required · All filled out forms for this template
        # has_matrix_field · Boolean · The form has matrix field
        # has_non_readonly_modules · Boolean · When true, the form has modules that the user has to fill out
        # id · ID! · required · The unique identifier of the module form
        # is_video · Boolean · Whether the form contains only one custom_module with mod_type 'video' and was created as part of a program
        # last_updated_by_user · User · User who last updated this form
        # metadata · String · A serialized JSON string of metadata. Maximum character limit of 10,000.
        # name · String · The given name of the template
        # prefill · Boolean · Whether subsequent times filling out the template, will start with the template prefilled with the previous answers
        # updated_at · String! · required · The date on which the template was updated
        # uploaded_by_healthie_team · Boolean! · required · Whether or not this form was uploaded by Healthie team member
        # use_for_charting · Boolean! · required · Whether the template can be used to chart with
        # use_for_program · Boolean! · required · Whether the template was made for a program
        # user · User · The owner of the template

        try:
            response = self._execute_request(mutation, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Groups

    def list_groups(self) -> Dict[str, Any]:
        query = """
query userGroups($offset: Int, $keywords: String, $sort_by: String) {
  userGroupsCount(keywords: $keywords)
  userGroups(offset: $offset, keywords: $keywords, sort_by: $sort_by, should_paginate: true) {
    id
    name
    users_count
  }
}
        """
        try:
            response = self._execute_request(query)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    def list_groups_with_users(self) -> Dict[str, Any]:
        query = """
query userGroups($offset: Int, $keywords: String, $sort_by: String) {
  userGroupsCount(keywords: $keywords)
  userGroups(offset: $offset, keywords: $keywords, sort_by: $sort_by, should_paginate: true) {
    id
    name
    users_count
    users{
      id
      name
    }
  }
}
        """
        try:
            response = self._execute_request(query)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Orders

    def list_orders(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
    query labOrders(
  $client_filter: String
  $client_id: ID
  $keywords: String
  $lab_filter: String
  $provider_filter: String
  $recent_orders: Boolean
  $offset: Int
  $sort_by: String
  $status_filter: String
) {
  labOrders(
    client_filter: $client_filter
    client_id: $client_id
    keywords: $keywords
    lab_filter: $lab_filter
    provider_filter: $provider_filter
    recent_orders: $recent_orders
    offset: $offset
    sort_by: $sort_by
    status_filter: $status_filter
  ) {
    id
    integration
    lab
    lab_company
    patient {
      id
      full_name
    }
    orderer {
      id
      full_name
    }
    status
    normalized_status
    test_date
    lab_results {
      id
      lab_observation_requests {
        id
        lab_analyte
        lab_observation_results {
          id
          units
          reference_range
          qualitative_result
          quantitative_result
          abnormal_flag
        }
      }
    }
  }
}        """
        try:
            response = self._execute_request(query, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Charts

    def list_charts(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
query chartNotes(
  $end_date: ISO8601Date
  $start_date: ISO8601Date
  $user_id: ID
  $provider_ids: [ID]
  $chart_note_status: ChartNoteStatus
  $custom_module_form_ids: [ID!]
  $exclude_requested_and_intake_flow_forms: Boolean
  $should_paginate: Boolean
  $offset: Int
  $page_size: Int
  $after: Cursor
) {
  chartNotes(
    end_date: $end_date
    start_date: $start_date
    user_id: $user_id
    provider_ids: $provider_ids
    chart_note_status: $chart_note_status
    custom_module_form_ids: $custom_module_form_ids
    exclude_requested_and_intake_flow_forms: $exclude_requested_and_intake_flow_forms
    should_paginate: $should_paginate
    offset: $offset
    page_size: $page_size
    after: $after
  ) {
    appointment {
      id
    }
    autoscored_sections {
      section_key
      section_title
      show
      value
    }
    chart_note_status
    charting_note_addendums {
      id
    }
    cms1500 {
      id
    }
    created_at
    current_summary {
      id
    }
    cursor
    custom_module_form {
      id
    }
    deleted_at
    documents {
      id
    }
    external_id
    filler {
      id
      name
    }
    finished
    form_answer_group_audit_events {
      id
    }
    form_answer_group_signings {
      id
    }
    form_answer_group_users_connections {
      id
    }
    form_answers {
      id
    }
    frozen
    group_appointment_attendees {
      id
    }
    id
    individual_client_notes {
      id
    }
    individual_note {
      id
    }
    is_group_appt_note
    is_locked
    locked_at
    locked_by {
      id
    }
    metadata
    name
    offering_with_recommended_products {
      id
    }
    provider_can_add_addendum
    provider_can_lock
    provider_can_sign
    provider_can_unlock
    record_created_at
    requested_form_completion {
      id
    }
    updated_at
    user {
      id
    }
    user_id
    versioning_stream_name
  }
}        """
        try:
            response = self._execute_request(query, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Faxes

    def list_faxes(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
        query sentFaxes(
  $keywords: String
  $order_by: SentFaxOrderKeys
  $offset: Int
  $page_size: Int
  $after: Cursor
) {
  sentFaxes(
    keywords: $keywords
    order_by: $order_by
    offset: $offset
    page_size: $page_size
    after: $after
  ) {
    created_at
    cursor
    destination_number
    id
    parsed_form_answer_group_ids
    patient {
      id
      name
    }
    resendable
    sender {
      id
      name
    }
    status
    status_display_string
    updated_at
  }
}
        """

        try:
            response = self._execute_request(query, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}

    # Notifications

    def list_notifications(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
query sentNotificationRecords(
  $end_date: String
  $offset: Int
  $org_level: Boolean
  $patient_id: ID
  $provider_id: ID
  $should_paginate: Boolean
  $start_date: String
  $status: String
  $type: String
) {
  sentNotificationRecords(
    end_date: $end_date
    offset: $offset
    org_level: $org_level
    patient_id: $patient_id
    provider_id: $provider_id
    should_paginate: $should_paginate
    start_date: $start_date
    status: $status
    type: $type
  ) {
    category
    created_at
    delivery_status
    id
    notification_description
    notification_type
    representation_type
    user_id
  }
}
"""
        try:
            response = self._execute_request(query, input_data)
            return response.get("data", {})
        except Exception as e:
            print(e)
            return {}
