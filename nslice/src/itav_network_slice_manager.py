from datetime import datetime, timezone
from datetime import datetime, timezone
import requests
import json

from config import Config


# Set up logging
logger = Config.setup_logging()

class ITAvNetworkSliceManager:
    
    # Set up logging
    #logger = Config.setup_logging()

    def __init__(self, base_url: str):
        self.base_url = base_url

    def enforce_network_slice(self, payload: dict):

        logger.info(
            "Will Enforce Network Slice with characteristics: "
            f"{json.dumps(payload, indent=4)}"
        )

        enforcement_result = {
            "currentRetries": 1,
            "success": None,
            "sliceManagerResponse": None,
            "lastOperationTimestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            response = requests.request(
                "POST",
                f"{self.base_url}/productOrder/post",
                headers= {
                    'Content-Type': 'application/json'
                },
                data= json.dumps(payload),
                timeout=10
            )
                        
            if response.status_code == 201:
                enforcement_result["success"] = True
                enforcement_result["sliceManagerResponse"] = str(response.json())
            else:
                enforcement_result["success"] = False
                resenforcement_resultult["sliceManagerResponse"] = str(response.json())

        except Exception as exception:
            logger.error(f"An Exception Ocurred: {exception}")
            enforcement_result["success"] = False
            enforcement_result["sliceManagerResponse"] = str(exception)

        logger.info(
            "Slice Manager API responded with status code: "
            f"{response.status_code}. Result: "
            f"{json.dumps(enforcement_result, indent=4)}"
        )

        return enforcement_result