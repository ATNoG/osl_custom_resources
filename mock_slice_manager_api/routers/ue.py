# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:49:45
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:08:41

from fastapi import APIRouter, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from schemas import ue as ue_schemas 
from auth.auth import authenticate
import logging

# start the router
router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)

@router.post(
    "/post",
    tags=["UE"],
    summary="Create a new UE and associate it with a slice",
    description="Create a new UE and associate it with a slice.",
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Created",
                        "data": {
                            "IMSI":1,
                            "numIMSIs":2,
                            "slice":"second_slice",
                            "IPV4":"",
                            "IPV6":"",
                            "AMDATA":True,
                            "DEFAULT":"TRUE",
                            "UEcanSendSNSSAI":"TRUE",
                            "AMBRUP":2000000,
                            "AMBRDW":2000000,
                            "id":1,
                            "operational_state":"ENABLED",
                            "SNSSAI":"1-222222",
                            "IMSIGroupNAME":"second_slice1"
                        }
                    }
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Error",
                        "reason": "unknown"
                    }
                }
            }
        },
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail":"Invalid authentication credentials"
                    }
                }
            }
        },
        
    }
)
def create_ue(
    ue: ue_schemas.UEBase,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    filtered_ue = {key: value for key, value in ue.dict().items()}

    # If IMSI == -1 -> return error
    if filtered_ue["IMSI"] == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Error", "reason": "uknown"}
        )
        
    filtered_ue["id"] = 1
    filtered_ue["operational_state"] = "ENABLED"
    filtered_ue["SNSSAI"] = "1-222222"
    filtered_ue["DNN"]: filtered_ue["slice"]
    filtered_ue["IMSIGroupNAME"] = filtered_ue["slice"] + \
        str(filtered_ue["IMSI"])
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"description": "Created", "data": filtered_ue})
