# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 16:08:06
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:14:51

from fastapi import APIRouter, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from schemas import netslice as netslice_schemas 
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
    tags=["productOrder"],
    summary="Create a new Network Slice Product Order",
    description="Create a new Network Slice Product Order",
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Created",
                        "data": {
                            "description":"Success",
                            "data":{
                                "coverage_area":{
                                    "IT":"Coverage Area Description"
                                },
                                "operational_state":"OperationalState.ENABLED",
                                "administrative_state":"AdministrativeState.UNLOCKED",
                                "sst":"1",
                                "sd":"222222",
                                "prioritylabel":"100",
                                "dllatency":"20",
                                "ullatency":"20",
                                "dlguathptperue":"20000.0",
                                "ulguathptperue":"20000.0",
                                "dlmaxthptperue":"50000.0",
                                "ulmaxthptperue":"50000.0",
                                "delaytolerance":"DelayTolerance.NOT_SUPPORTED",
                                "reliability":"99.9",
                                "dldeterministiccomm":"DeterministicCommAvailability.NOT_SUPPORTED",
                                "uldeterministiccomm":"DeterministicCommAvailability.NOT_SUPPORTED",
                                "nn6protection":[],
                                "dnn":"5gasp.eu",
                                "name":"5gasp",
                                "id":"5GASPHigh",
                                "n6protection":[]
                            }
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
async def create_product_order(
    product_order: netslice_schemas.NetworkSliceCreate,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # Convert product_order to a dictionary, including empty lists and dicts but excluding None
    # Cast non-list and non-dict values to strings
    filtered_product_order = {
        key: str(value) if not isinstance(value, (list, dict)) else value
        for key, value in product_order.dict().items()
        if value is not None or isinstance(value, (list, dict))
    }

    # If name == error -> return error
    name = filtered_product_order.get("name") \
        if filtered_product_order.get("name") \
        else filtered_product_order.get("id")

    if name.lower() == "error":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Error", "reason": "uknown"}
        )


    # Transform coverage_area to the required dictionary format with a fixed description
    coverage_area = filtered_product_order.get("coverage_area", [])
    filtered_product_order["coverage_area"] = {
        area: "Coverage Area Description" for area in coverage_area
    }

    # Remove None values within each rule in the n6protection list
    filtered_product_order["n6protection"] = [
        {k: v for k, v in rule.items() if v is not None} 
        for rule in filtered_product_order.get("n6protection", [])
    ]

    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"description": "Success", "data": filtered_product_order})


