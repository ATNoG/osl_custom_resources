# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-25 08:10:27
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 10:38:16
from datetime import datetime, timezone
from datetime import datetime, timezone
import requests
import json
import time

from config import Config


# Set up logging
logger = Config.setup_logging()

class ITAvNetworkSliceManager:

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def create_ue(self, spec: dict, payload: dict):

        logger.info("Checking if the Network Slice UE should be created...")

        enforcement_data = spec["itav-ue-enforcement"]

        # If Network Slice was already enforced, return
        if enforcement_data.get("success"):
            logger.info("Network Slice UE already created")
            return False, None
        

        # If it is the first time this operation is running, enforce
        if not enforcement_data.get("firstOperationTimestamp"):
            
            first_operation_ts = datetime.now(timezone.utc).isoformat()

            enforcement_result = {
                "currentRetries": 0,
                "firstOperationTimestamp": first_operation_ts,
                "lastOperationTimestamp": first_operation_ts
            }
            
            self.__create_ue_on_slice_manager(
                payload, enforcement_result
            )

            return True, enforcement_result

        # If it is not the first time, check if it needs to be updated
        elif enforcement_data["retryOnFail"]:
            if enforcement_data["maxRetries"] > enforcement_data.get(
                "currentRetries"
            ):
                logger.info(
                    "Will retry to create the Network Slice UE in "
                    f"{enforcement_data['waitTimeBeforeRetrying']} seconds"
                )

                time.sleep(enforcement_data['waitTimeBeforeRetrying'])

                enforcement_result = {
                    "currentRetries": enforcement_data["currentRetries"] + 1,
                    "lastOperationTimestamp": datetime.now(timezone.utc)
                        .isoformat()
                }
                
                self.__create_ue_on_slice_manager(
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
        
    
    def __create_ue_on_slice_manager(
            self, payload: dict, enforcement_result: dict
        ):

        logger.info(
            "Will Try to Creaet a Network Slice UE with Characteristics: "
            f"{json.dumps(payload, indent=4)}"
        )

        try:
            response = requests.request(
                "POST",
                f"{self.base_url}/UE/post",
                headers= {
                    'Content-Type': 'application/json'
                },
                auth=(self.username, self.password),
                data= json.dumps(payload),
                timeout=120
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