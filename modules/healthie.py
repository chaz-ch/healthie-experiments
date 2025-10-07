import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

# --- Module-Level Constant ---
# NOTE: Replace this with the actual URL of your secure GraphQL API
TARGET_GRAPHQL_URL = "https://staging-api.gethealthie.com/graphql"

class Healthie:
    """
    A client class for managing authenticated connections and operations 
    to Healthie.
    """

    def __init__(self, api_key: str):
        """
        Initializes the secure GraphQL client with authentication.
        """
        if not api_key:
            raise ValueError("API Key must be provided.")
            
        self.endpoint = TARGET_GRAPHQL_URL
        self.api_key = api_key

        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "AuthorizationSource": "API"
        }

    def _execute_request(self, query: str, variables: Optional[Dict[str, Any]] = None,timeout: int = 10) -> Dict[str, Any]:
        
        payload: Dict[str, Any] = {"query": query}
        if variables is not None:
            payload["variables"] = variables
            
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self.headers,
                timeout=timeout
            )
            response.raise_for_status() 
            
            data: Dict[str, Any] = response.json()
            
            if 'errors' in data:
                error_messages: List[str] = [err.get('message', 'Unknown GraphQL Error') for err in data['errors']]
                raise ValueError(f"GraphQL Query Error(s): {'; '.join(error_messages)}")

            return data

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"API Request Error: {e}")

    def _execute_upload_request(self, data: Dict[str, Any], files: Dict[str, Any],timeout: int = 10) -> Dict[str, Any]:

        try:
            response = requests.post(
                self.endpoint, 
                data = data,
                files = files,
                headers = self.headers,
                timeout=timeout
            )

            response.raise_for_status() 
            
            data: Dict[str, Any] = response.json()
            
            if 'errors' in data:
                error_messages: List[str] = [err.get('message', 'Unknown GraphQL Error') for err in data['errors']]
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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
}        """

        try:
            response = self._execute_request(mutation, input_data)
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        inputs = {
            'ids': tag_ids, 
            'taggable_user_id': user_id
        }
        
        try:
            response = self._execute_request(mutation, inputs)
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        inputs = {
            'id': tag_id, 
            'taggable_user_id': user_id
        }
        
        try:
            response = self._execute_request(mutation, inputs)
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        except Exception as e:
            print(e)
        return response.get('data', {})

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
        inputs = {
            'id': tag_id
        }
        
        try:
            response = self._execute_request(mutation, inputs)
        except Exception as e:
            print(e)
        return response.get('data', {})

# document-related

    def create_document(self, variables: Dict[str, Any]) -> Dict[str, Any]:

        if variables['display_name'] is None:
            temp_file = Path(variables['file_path'])
            variables['display_name'] = temp_file.stem
        
        file = open(variables['file_path'], 'rb')

        inputs = {
            'file:': None, # Upload

            'display_name:': variables['display_name'], 
            'clients_ids:': variables['clients_ids'],
            'provider_ids:': variables['provider_ids'],
            
        }
        

        mutation = """
        mutation createDocument(
            $file: Upload, 
            $display_name: String, 
            $clients_ids: String,
            $provider_ids: [String],

            ) {
          createDocument(input: { 
            file: $file,
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


        # inputs["folder_id"] = variables['folder_id']

        operations = json.dumps({
            "query": mutation,
            "variables": inputs
        })
        
        map = json.dumps({ "0": ["variables.file"] })

        data = {
            "operations": operations,
            "map": map
        }
        
        files = {
            "0" : file
        }
        
        response = self._execute_upload_request(
            data,
            files
        )

        return response.get('data', {})

    # def create_note(self, variables: Dict[str, Any]) -> Dict[str, Any]:

    #     if variables['display_name'] is None:
    #         temp_file = Path(variables['file_path'])
    #         variables['display_name'] = temp_file.stem
        
    #     inputs = {
    #         'file:': None, 
    #         'display_name:': None, 
    #         'folder_id:': None,
    #         'clients_ids:': None,

    #         'care_plan_id:': None,
    #         'course_id:': None,
    #         'description:': None,
    #         'file_string:': None,
    #         'from_date:': None,
    #         'from_program_create:': None,
    #         'generate_ccda_for_rel_user_id:': None,
    #         'generate_human_readable_ccda_for_rel_user_id:': None,
    #         'include_in_charting:': None,
    #         'is_photo_id:': None,
    #         'metadata:': None,
    #         'on_form_for_user_id:': None,
    #         'org_level:': None,
    #         'payout_id:': None,
    #         'provider_ids:': None,
    #         'rcf_id:': None,
    #         'rel_user_id:': None,
    #         'report_type:': None,
    #         'share_users:': None,
    #         'share_with_rel:': None,
    #         'to_date': None
            
    #     }
        
    #     file = open(variables['file_path'], 'rb')

    #     mutation = """
    #     mutation createNote($input: createNoteInput) {
    #         createNote(input: $input) {
    #             messages
    #             note
    #         }
    #     }
    #     """

    #     inputs["display_name"] = variables['display_name']

    #     # inputs["folder_id"] = variables['folder_id']

    #     cleaned_inputs = {k: v for k, v in inputs.items() if v is not None}

    #     cleaned_inputs["file"] = None

    #     operations = json.dumps({
    #         "query": mutation,
    #         "variables": cleaned_inputs
    #     })
        
    #     map = json.dumps({ "0": ["cleaned_inputs.file"] })

    #     data = {
    #         "operations": operations,
    #         "map": map
    #     }
        
    #     files = {
    #         "0" : file
    #     }
        
    #     response = self._execute_upload_request(
    #         data,
    #         files
    #     )

    #     return response.get('data', {})

    def create_conversation(self, variables: Dict[str, Any]) -> Dict[str, Any]:

        mutation = """
            mutation createConversation(
            $input: createConversationInput
            ) {
            createConversation(input: $input) {
                conversation {
                    id
                    name
                }
            }
            }
        """

        # inputs = {
        #     "name": variables['conversation_name'],
        #     "owner_id": variables['owner_id'],
        #     "note": {
        #         "attached_document": None, # Upload
        #         "content": None
        #     },
        #     "simple_added_users": variables['client_id'],
        # }
        
        inputs = {
            "name": variables['conversation_name'],
            "owner_id": variables['owner_id'],
            "note": None,
            "simple_added_users": variables['client_id'],
        }

        # file = open(variables['file_path'], 'rb')

        # inputs["note"]["attached_document"] = None

        # operations = json.dumps({
        #     "query": mutation,
        #     "variables": inputs
        # })
        
        # map = json.dumps({ "0": ["inputs.note.attached_document"] })

        # data = {
        #     "operations": operations,
        #     "map": map
        # }
        
        # files = {
        #     "0" : file
        # }
        
        # response = self._execute_request(
        #     data,
        #     files
        # )

        try:
            response = self._execute_request(mutation, inputs)
        except Exception as e:
            print(e)
        return response.get('data', {})

        return response.get('data', {})

