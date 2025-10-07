import requests
import json
from typing import Optional, Dict, Any, List

# --- Module-Level Constant ---
# NOTE: Replace this with the actual URL of your secure GraphQL API
TARGET_GRAPHQL_URL = "https://your-secure-graphql-api.com/graphql"

class SecureGraphQLClient:
    """
    A client class for managing authenticated connections and operations 
    to a GraphQL API endpoint, supporting nested input and output structures.
    """

    def __init__(self, api_key: str, auth_scheme: str = "Bearer"):
        """Initializes the secure GraphQL client with authentication."""
        if not api_key:
            raise ValueError("API Key must be provided.")
            
        self.endpoint = TARGET_GRAPHQL_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{auth_scheme} {api_key}"
        }

    def _execute_request(self, 
                         query: str, 
                         variables: Optional[Dict[str, Any]] = None,
                         timeout: int = 10) -> Dict[str, Any]:
        """Internal core method to handle the POST request execution."""
        
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

# --------------------------------------------------------------------------
# Query and Mutation Methods
# --------------------------------------------------------------------------

    def query(self, query_name: str, arguments: str, return_fields: str) -> Dict[str, Any]:
        """
        Executes a generic GraphQL QUERY for fetching data.

        :param query_name: The root query field (e.g., 'getUser').
        :param arguments: The arguments for the query (e.g., '(id: $id)'). Must include variable definitions if needed.
        :param return_fields: A string of fields, possibly nested, to retrieve (e.g., 'id name profile { bio url }').
        :return: The 'data' section of the GraphQL response.
        """
        # Note: This simple structure assumes arguments are handled outside this method 
        # or the query is static. For full variable support, see below.
        
        # A more robust query builder for variable handling:
        # We assume `query_name` is also the function being called inside the braces.
        # This requires the user to pass a full definition of variables like "$id: ID!" 
        # as part of the `arguments` string.
        
        query = f"""
            query Get{query_name.capitalize()}({arguments}) {{
                {query_name}({arguments.split(':', 1)[0].replace('$', '')}) {{
                    {return_fields}
                }}
            }}
        """
        # This is overly simplified. A common pattern is:
        # query { query_name(id: "123") { ... } }
        # Let's simplify the function signature for demonstration:
        
        raise NotImplementedError("Use the execute_query_operation method for full control.")


    def execute_query_operation(self, operation: str, operation_name: str, 
                                variable_definitions: str, arguments: str, 
                                variables_data: Dict[str, Any], return_fields: str) -> Dict[str, Any]:
        """
        Executes a flexible GraphQL operation (query or mutation) with full control 
        over variable definitions and arguments, supporting nested output.

        :param operation: 'query' or 'mutation'.
        :param operation_name: The name of the function on the GraphQL server (e.g., 'getUser' or 'createUser').
        :param variable_definitions: String defining variables (e.g., "$id: ID!").
        :param arguments: Arguments passed to the function (e.g., "id: $id").
        :param variables_data: The dictionary containing the actual variable values.
        :param return_fields: The fields to return (e.g., "id name messages { field message }").
        :return: The 'data' section of the GraphQL response.
        """
        
        # Build the operation string
        query = f"""
            {operation} {operation_name}Wrapper({variable_definitions}) {{
                {operation_name}({arguments}) {{
                    {return_fields}
                }}
            }}
        """
        
        response = self._execute_request(query, variables_data)
        return response.get('data', {})


    # --------------------------------------------------------------------------
    # CRUD Operations leveraging the new execute_query_operation
    # --------------------------------------------------------------------------

    def create(self, mutation_name: str, input_type: str, input_data: Dict[str, Any], 
               return_fields: str = "id success") -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to CREATE a new resource, supporting nested output.
        """
        return self.execute_query_operation(
            operation='mutation',
            operation_name=mutation_name,
            variable_definitions=f"$input: {input_type}!",
            arguments="input: $input",
            variables_data={"input": input_data},
            return_fields=return_fields
        )

    def modify(self, mutation_name: str, input_type: str, input_data: Dict[str, Any], 
               return_fields: str = "id success") -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to MODIFY (UPDATE) an existing resource, supporting nested output.
        """
        return self.execute_query_operation(
            operation='mutation',
            operation_name=mutation_name,
            variable_definitions=f"$input: {input_type}!",
            arguments="input: $input",
            variables_data={"input": input_data},
            return_fields=return_fields
        )
    
    def deactivate(self, mutation_name: str, resource_id: str, 
                   return_fields: str = "success") -> Dict[str, Any]:
        """
        Executes a GraphQL mutation to DEACTIVATE (or delete) a resource by ID, supporting nested output.
        """
        return self.execute_query_operation(
            operation='mutation',
            operation_name=mutation_name,
            variable_definitions="$id: ID!",
            arguments="id: $id",
            variables_data={"id": resource_id},
            return_fields=return_fields
        )

    # Document upload remains a placeholder for complex multipart logic
    def document_upload(self, upload_mutation: str, file_path: str, resource_id: str) -> Dict[str, Any]:
        """
        Handles GraphQL file upload. (Placeholder for real multipart logic.)
        """
        print("⚠️ NOTE: Document upload requires dedicated multipart/form-data handling. Using simplified JSON mutation.")
        
        return self.execute_query_operation(
            operation='mutation',
            operation_name=upload_mutation,
            variable_definitions="$id: ID!, $fileName: String!",
            arguments="id: $id, fileName: $fileName",
            variables_data={"id": resource_id, "fileName": file_path.split('/')[-1]},
            return_fields="success uploadUrl"
        )

# --------------------------------------------------------------------------
# Example Usage Demonstrating Nested Output
# --------------------------------------------------------------------------

if __name__ == '__main__':
    MOCK_API_KEY = "dummy_secret_key_123"

    try:
        client = SecureGraphQLClient(api_key=MOCK_API_KEY)
        print("Client initialized. Target URL:", client.endpoint)
        
        # --- 1. Query with Nested Output ---
        
        # 1a. Define the nested output fields as a single string
        NESTED_OUTPUT_FIELDS = """
            id 
            username
            messages { 
                field 
                content 
                timestamp
            }
        """

        # 1b. Define variables for the query
        query_variables_data = {"id": "u456"}
        
        print("\n--- Testing Nested Output (Query) ---")
        
        # We use the generic execution method to run a QUERY
        # try:
        #     result = client.execute_query_operation(
        #         operation='query',
        #         operation_name='getUserWithMessages',
        #         variable_definitions='$id: ID!',
        #         arguments='id: $id',
        #         variables_data=query_variables_data,
        #         return_fields=NESTED_OUTPUT_FIELDS
        #     )
        #     print("\nServer Response (Mocked):", json.dumps(result, indent=2))
        # except Exception as e:
        #     print(f"Error during mock query: {e}")
        
        print("Expected Nested Output Fields:")
        print(NESTED_OUTPUT_FIELDS)
        
        # --- 2. Mutation (Create) with Nested Output ---

        MUTATION_OUTPUT_FIELDS = """
            id 
            createdAt
            owner { 
                id 
                name 
            }
        """
        # try:
        #     result = client.create(
        #         mutation_name="createPost", 
        #         input_type="CreatePostInput", 
        #         input_data={"title": "New Post", "content": "Hello"}, 
        #         return_fields=MUTATION_OUTPUT_FIELDS
        #     )
        #     print("\nServer Response (Mocked Create):", json.dumps(result, indent=2))
        # except Exception as e:
        #     print(f"Error during mock mutation: {e}")
        
        print("\nNOTE: Actual requests are commented out. The ability to produce nested output comes from passing the nested string (e.g., 'messages { field content }') to the `return_fields` parameter.")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")