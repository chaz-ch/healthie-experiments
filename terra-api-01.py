import json
import requests

response = requests.post(
    "https://api.tryterra.co/v2/auth/generateWidgetSession",
    headers={
        "x-api-key": "5LqwV9aaSICe770M8gXe3lsxsBeu6Jjd",
        "Content-Type": "application/json",
    },
    data=json.dumps(
        {
            "providers": "GARMIN,FITBIT,OURA,WITHINGS,SUUNTO",
            "language": "en",
            "reference_id": "user123@email.com",
            "auth_success_redirect_url": "https://myapp.com/success",
            "auth_failure_redirect_url": "https://myapp.com/failure",
        }
    ),
)

data = response.json()
