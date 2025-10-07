import requests
import json

# The URL of the GraphQL API endpoint
API_URL = "https://staging-api.gethealthie.com/graphql"
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# 1. Define the GraphQL Query
# This query fetches the first 5 characters and their episodes from the API
GRAPHQL_QUERY = """
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

# 2. Prepare the request payload
# The query is sent as a JSON object under the 'query' key.

variables = {
    "should_paginate": False
}

payload = {
    "query": GRAPHQL_QUERY,
    "variables": variables
}

auth_headers = {
    "Authorization": f"Basic {API_KEY}",
    "AuthorizationSource": "API"
}


# 3. Send the POST request
try:
    response = requests.post(API_URL, json=payload, headers=auth_headers)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # 4. Process the JSON response
    data = response.json()
    
    # Check if there are any errors in the GraphQL response
    if 'errors' in data:
        print("GraphQL Errors:")
        for error in data['errors']:
            print(f"- {error['message']}")
    
    # Access the actual data
    elif 'data' in data:
        print("--- GraphQL Data ---")
        print(f"{data['data']['usersCount']} users retrieved")
        users = data['data']['users']
        for user in users:
            print(f"ID: {user['id']}")
                        
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON response.")
    
