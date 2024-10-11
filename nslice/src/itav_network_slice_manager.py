from datetime import datetime, timezone
import requests
import json
from config import Config


class ITAvNetworkSliceManager:
    
    # Set up logging
    #logger = Config.setup_logging()

    def __init__(self, base_url: str):
        self.base_url = base_url

    #def enforce_profile(self, profile: str):
    #    self.logger.info(f"Will Enforce the Profile: {profile}")
    #    result = {
    #        "success": None,
    #        "enforced-profile": None,
    #        "timestamp": None,
    #        "result": None
    #    }
#
    #    try:
    #        response = requests.request(
    #            "PATCH",
    #            f"{self.base_url}/productOrder/{profile}/patch",
    #            headers= {
    #                'Content-Type': 'application/json'
    #            },
    #            data= json.dumps({
    #                "administrative_state": "UNLOCKED",
    #                "operational_state": "ENABLED"
    #            }),
    #            timeout=10
    #        )
    #        
    #        self.logger.info(f"After Request")
    #        
    #        if response.status_code == 200:
    #            result["success"] = True
    #            result["enforced-profile"] = profile
    #            result["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    #            result["result"] = str(response.json())
#
    #        else:
    #            result["success"] = False
    #            result["enforced-profile"] = profile
    #            result["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    #            result["result"] = str(response.json())
#
    #    except Exception as exception:
    #        self.logger.error(f"Exception: {exception}")
    #        result["success"] = False
    #        result["enforced-profile"] = profile
    #        result["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    #        result["result"] = str(exception)
#
    #    return result
