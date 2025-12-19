import requests
import time
import statistics
from datetime import datetime
import warnings

# Suppress the InsecureRequestWarning that appears when using verify=False
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

# --- Configuration ---
# The URL from the curl request
TARGET_URL = "https://perf.cascaidhealth.com:8446/hl7"
# The number of times to repeat the request
NUM_REQUESTS = 1000
# Delay between requests in seconds
DELAY_BETWEEN_REQUESTS = 0
# --- End Configuration ---

# --- Custom Request Details ---

# 1. Custom Headers (MIMICS: --header 'Content-Type: text/plain')
CUSTOM_HEADERS = {
    "Content-Type": "text/plain",
    "User-Agent": "HL7RepeatedTestScript/1.0",
}

# 2. Raw Data Payload (MIMICS: --data-raw '...')
# This is the exact HL7 message content from your curl command.
RAW_DATA_PAYLOAD = """
MSH|^~\&|EXA|EXA|COREPOINT|COREPOINT|20250516000115||ORM^O01^ORM_O01|663831336||2.5.1|||AL||||EVN|O01|20250516000115||||||||||PID||T10488785^^^^SimonMed AZ Phoenix||T10488785|Opendr^Levis^^||19800609|M|||111 times square^^PHOENIX^AZ^85045^usa||(333)435-2524^HP~(333)654-5234^CP~^NET^^levis@mailcatch.com|||Married||T10488785||^^||||||||||PD1|1||||PV1|1||91^MR(3T)-Phoenix^48^SimonMed AZ Phoenix^48MR^|||||66703^AARON^GILA^^^1457352965^16468^425 W 59th St^Ste 5F^New York^NY^10019|66703^AARON^GILA^^^1457352965^16468||||||||||||||||||||||||||||||^||||||ORC|ORD|43962150|43962150||ORD||30^^^^||20250515235640|Patmase, Ragini||66703^AARON^GILA^^^1457352965^16468|||||SimonMed AZ PhoenixOBR|1|43962150|43962150|74181^ABDOMEN WITHOUT CONTRAST||||||||||||66703^AARON^GILA^^^1457352965^16468||||||||MR|ORD||30^^^^|||||||||||||||||85||||||IN1|1FT1|1|43962150||||CHG|74181|||||||||||||66703^AARON^GILA^^^1457352965^16468|||43962150||74181^ ABDOMEN WITHOUT CONTRAST|~~|PR1|1||74181^1^43962150| ABDOMEN WITHOUT CONTRAST^MR^|||||||||||NTE|1
"""
# --- End Custom Request Details ---


def send_repeated_post_requests(url, num_requests, delay, headers, payload):
    """
    Sends repeated POST requests with custom headers and raw data payload,
    tracking time and status.
    """

    print(f"🚀 Starting POST request test for: {url}")
    print(f"Total requests to be sent: {NUM_REQUESTS}")
    # Display the first 80 characters of the payload for verification
    print(f"Payload (HL7 Sample): {payload[:80].strip()}...\n")
    print("--- WARNING: SSL verification is DISABLED (`verify=False`) ---")
    print("This mimics the `curl -k` flag and should ONLY be used for testing.")
    print("----------------------------------------------------------------\n")

    # Data structures to store results
    response_times = []
    status_code_counts = {}

    for i in range(1, num_requests + 1):
        # 1. Start timer
        start_time = time.time()

        try:
            # 2. Send the POST request
            # IMPORTANT: data=payload sends the raw string body.
            # IMPORTANT: verify=False mimics the curl -k (insecure) flag.
            response = requests.post(
                url, headers=headers, data=payload, timeout=15, verify=False
            )

            # 3. Stop timer and calculate duration
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds

            # 4. Record results
            status_code = response.status_code
            response_times.append(duration)
            status_code_counts[status_code] = status_code_counts.get(status_code, 0) + 1
            result_status = "SUCCESS" if 200 <= status_code < 300 else "FAIL"

        except requests.exceptions.RequestException as e:
            # 5. Handle network/request errors
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            status_code = "N/A"
            error_msg = str(e).splitlines()[0]
            result_status = f"ERROR: {error_msg}"

        # Log individual request
        print(
            f"Request {i:<6}: Status={status_code:<3} | Time={duration:.2f}ms | Result={result_status}"
        )

        # Apply delay before the next request
        if i < num_requests:
            time.sleep(delay)

    # --- Summary Statistics ---
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("=" * 50)

    total_requests_sent = num_requests

    # Calculate successful requests (2xx status codes)
    successful_requests = sum(
        count
        for code, count in status_code_counts.items()
        if isinstance(code, int) and 200 <= code < 300
    )

    # Report basic counts
    print(f"Total Requests Sent: {total_requests_sent}")
    print(f"Successful Requests (2xx): {successful_requests}")
    print(f"Failed/Errored Requests: {total_requests_sent - successful_requests}")

    # Report Status Codes
    print("\nStatus Code Counts:")
    for code, count in sorted(status_code_counts.items()):
        print(f"- HTTP {code}: {count} times")

    # Report Time Statistics (only for successfully timed requests)
    if response_times:
        print("\nResponse Time (ms) Statistics:")
        print(f"- Minimum Time: {min(response_times):.2f}ms")
        print(f"- Maximum Time: {max(response_times):.2f}ms")
        print(f"- Average Time: {statistics.mean(response_times):.2f}ms")
        if len(response_times) >= 2:
            print(f"- Median Time: {statistics.median(response_times):.2f}ms")
    else:
        print("\nNo successful response times to report.")


if __name__ == "__main__":
    start = datetime.now()
    send_repeated_post_requests(
        TARGET_URL,
        NUM_REQUESTS,
        DELAY_BETWEEN_REQUESTS,
        CUSTOM_HEADERS,
        RAW_DATA_PAYLOAD,
    )
    end = datetime.now()
    duration = end - start
    print(f"\n⏱️ Total Test Duration: {duration}")

# ### **How to Run the Script**

# 1.  **Install Requests:** If you haven't already, install the necessary library:
#     ```bash
#     pip install requests
#     ```
# 2.  **Save:** Save the code above as a Python file (e.g., `hl7_monitor.py`).
# 3.  **Configure:** Adjust `TARGET_URL`, `NUM_REQUESTS`, and `DELAY_BETWEEN_REQUESTS` if needed.
# 4.  **Execute:** Run the script from your terminal:
#     ```bash
#     python hl7_monitor.py
#     ```

# This script will output the status code and response time for each request, followed by a summary of the test.
