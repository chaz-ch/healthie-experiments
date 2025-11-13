from modules.healthie import Healthie
from alive_progress import alive_bar

PAGE_SIZE = 50  # The number of users to request per page (determine the server's limit)

PROD_PROVIDERS = {
    "10410358": "Karam Elabd",
    "10578403": "Tim Herby",
    "10666933": "Bridget Krueger",
    "10578423": "Rakesh Patel",
    "11008105": "Janelle Scachetti",
    "11008180": "Andrea Stage",
    "10578357": "Johann Windt",
    # 10410358 Karam Elabd          karam@cascaidhealth.com
    # 10578403 Tim Herby            tim@cascaidhealth.com
    # 10666933 Bridget Krueger      bridget@cascaidhealth.com
    # 10578423 Rakesh Patel         rakesh@cascaidhealth.com
    # 11008105 Janelle Scachetti    janelle@cascaidhealth.com
    # 11008180 Andrea Stage         andrea@cascaidhealth.com
    # 10578357 Johann Windt         johann@cascaidhealth.com
}


def main():
    H = Healthie("PROD")

    invite_count = 0
    provider_counts = {}

    for provider_id in PROD_PROVIDERS:
        invites = 0
        offset = 0
        all_notification_records = []

        print(f"Provider: {provider_id} {PROD_PROVIDERS[provider_id]}")
        print("---------------------------------")

        # Loop until a page returns fewer results than the limit (PAGE_SIZE)
        more_to_get = True

        with alive_bar(
            0,
            dual_line=True,
            title="retrieving notification records",
        ) as bar:
            while more_to_get:
                # Define the variables for the current query
                variables = {
                    "org_level": False,
                    "should_paginate": True,
                    "provider_id": provider_id,
                    "type": "other",
                    "offset": offset,
                }

                response = H.list_notifications(variables)

                if "sentNotificationRecords" in response:
                    sent_notification_records = response["sentNotificationRecords"]

                    num_records = len(sent_notification_records)
                    offset += num_records

                    all_notification_records.extend(sent_notification_records)
                    bar.text = (
                        f"offset {offset}. Total: {len(all_notification_records)}"
                    )
                else:
                    sent_notification_records = None

                if not sent_notification_records:
                    bar.text = "No more notifications to fetch. Loop complete."
                    more_to_get = False

                bar()

        # processed_notification_records = []
        notification_count = len(all_notification_records)

        with alive_bar(
            notification_count,
            dual_line=True,
            title="processing notification records",
        ) as bar:
            for notification_record in all_notification_records:
                notification_type = notification_record["notification_type"]
                # notification_category = notification_record["category"]
                # notification_target = notification_record["user_id"]
                if notification_type == "client_invited_to_healthie":
                    invites += 1

                bar()

        provider_counts[provider_id] = {"invites": invites}

        invite_count += invites

        print("================================")

    print(f"Total invites: {invite_count}")

    for provider_id in provider_counts:
        print(
            f"Provider: {provider_id} {PROD_PROVIDERS[provider_id]:18} - invites: {provider_counts[provider_id]['invites']:2}"
        )


if __name__ == "__main__":
    main()
