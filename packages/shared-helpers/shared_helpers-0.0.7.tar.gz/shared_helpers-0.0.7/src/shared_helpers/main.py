import shared_helpers.variables as variables
from shared_helpers.yandex.organization.organization_helper import CloudHelper
from shared_helpers.yandex.tracker.tracker_helper import TrackerHelper
from shared_helpers.lm.sbbid.sbbid_helper import SbbIdHelper
from shared_helpers.functions import TokenHelper

token_helper = TokenHelper()

def fetch_current_iam_token() -> str:
    """Fetch a valid IAM token or return None."""
    token = None
    if (
        variables.SA01_IAM_TOKEN and
        variables.SA01_IAM_TOKEN_EXPIRY and
        int(variables.SA01_IAM_TOKEN_EXPIRY) <300
    ):
        print('using token from env')
        token = variables.SA01_IAM_TOKEN
    elif (variables.SA01_API_KEY and variables.SA01_CF_ENDPOINT_URL):
        print('using token from endpoint')
        token = token_helper.get_iam_token_from_endpoint(api_key=variables.SA01_API_KEY, endpoint_url=variables.SA01_CF_ENDPOINT_URL)
    elif token_helper.file_exists(json_file_path=variables.SA01_JSON_FILE_PATH):
        print('using token from file')
        token = token_helper.get_iam_token_from_file(json_file_path=variables.SA01_JSON_FILE_PATH)
    return token

if token := fetch_current_iam_token():
    cloud_client = CloudHelper(token)
    tracker_client = TrackerHelper(token)
sbbid_client = SbbIdHelper(x_api_key=variables.SBBID_X_API_KEY, environment = variables.SBBID_ENVIRONMENT)

#print(cloud_client.cloud_get_all_groups())
#print(tracker_client.queues_get_queues())
#print(sbbid_client.get_domains())