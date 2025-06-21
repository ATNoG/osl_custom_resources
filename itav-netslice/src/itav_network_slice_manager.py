# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-11 14:15:50
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:57:02
from datetime import datetime, timezone
from datetime import datetime, timezone
import requests
import json
import time

from config import Config


# Set up logging
logger = Config.setup_logging()

class ITAvNetworkSliceManager:
    
    # Set up logging
    #logger = Config.setup_logging()

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def enforce_network_slice(self, spec: dict, payload: dict):

        logger.info("Checking if the network slice should be enforced...")

        enforcement_data = spec["itav-netslice-enforcement"]

        # If Network Slice was already enforced, return
        if enforcement_data.get("success"):
            logger.info("Network Slice already enforced")
            return False, None
        

        # If it is the first time this operation is running, enforce
        if not enforcement_data.get("firstOperationTimestamp"):
            
            first_operation_ts = datetime.now(timezone.utc).isoformat()

            enforcement_result = {
                "currentRetries": 0,
                "firstOperationTimestamp": first_operation_ts,
                "lastOperationTimestamp": first_operation_ts
            }
            
            self.enforce_network_slice_on_manager(
                payload, enforcement_result
            )

            return True, enforcement_result

        # If it is not the first time, check if it needs to be updated
        elif enforcement_data["retryOnFail"]:
            if enforcement_data["maxRetries"] > enforcement_data.get(
                "currentRetries"
            ):
                logger.info(
                    "Will retry to enforce the Network Slice in "
                    f"{enforcement_data['waitTimeBeforeRetrying']} seconds"
                )

                time.sleep(enforcement_data['waitTimeBeforeRetrying'])

                enforcement_result = {
                    "currentRetries": enforcement_data["currentRetries"] + 1,
                    "lastOperationTimestamp": datetime.now(timezone.utc)
                        .isoformat()
                }
                
                self.enforce_network_slice_on_manager(
                    payload, enforcement_result
                )
                return True, enforcement_result

            else:
                logger.info(
                    "Will not retry again to enforce the Network Slice. "
                    "Maximum amount of retries has been reached."
                )
        else:
            logger.info(
                    "No retries are allowed to enforce the Network Slice."
                )
            
        return False, None
        
    
    def enforce_network_slice_on_manager(
            self, payload: dict, enforcement_result: dict
        ):

        logger.info(
            "Will Try to Enforce Network Slice with Characteristics: "
            f"{json.dumps(payload, indent=4)}"
        )

        try:
            response = requests.request(
                "POST",
                f"{self.base_url}/productOrder/post",
                headers= {
                    'Content-Type': 'application/json'
                },
                auth=(self.username, self.password),
                data= json.dumps(payload),
                timeout=300
            )
                        
            if response.status_code == 201:
                enforcement_result["success"] = True
                enforcement_result["sliceManagerResponse"] = {
                    "success": True,
                    "payload": str(response.json()),
                    "message": None
                }
            else:
                enforcement_result["success"] = False
                enforcement_result["sliceManagerResponse"] = {
                    "success": False,
                    "payload": str(response.json()),
                    "message": None
                }

            logger.info(
                "Slice Manager API responded with status code: "
                f"{response.status_code}. Result: "
                f"{json.dumps(enforcement_result, indent=4)}"
            )

        except Exception as exception:
            logger.error(f"An Exception Ocurred: {exception}")
            enforcement_result["success"] = False
            enforcement_result["sliceManagerResponse"] = {
                    "success": False,
                    "payload": str({}),
                    "message": f"An exception occurred: {exception}"
                }

            logger.error(
                f"An exception occurred: {exception}. Result: "
                f"{json.dumps(enforcement_result, indent=4)}"
            )