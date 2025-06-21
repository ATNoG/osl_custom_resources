# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-11 16:29:17
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 11:04:06
# Fully Generated with AI

from fastapi import FastAPI, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from typing import Optional
from fastapi.responses import JSONResponse
from auth.auth import authenticate
from schemas import netslice as netslice_schemas
from routers import ue as ue_router
import logging


# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

fast_api_tags_metadata = [
    {
        "name": "UE",
        "description": "Operations related with UEs.",
    },
]

fast_api_description = "ITAv's 5G Slice Management API Mock"


app = FastAPI(
    title="Slice Management API Mock",
    description=fast_api_description,
    version="0.0.1",
    contact={
        "name": "Rafael Direito",
        "email": "rdireito@av.it.pt",
    },
    openapi_tags=fast_api_tags_metadata
)

app.include_router(ue_router.router, prefix="/UE", tags=["UE"])





# Define the N6Protection model with additional optional fields
#class N6Protection(BaseModel):
#    type: Optional[str] = None
#    name: Optional[str] = None
#    priority: Optional[int] = None
#    ServerIP: Optional[str] = None
#    MaskLen: Optional[int] = None
#    startport: Optional[int] = None
#    endport: Optional[int] = None
#    ULGBR: Optional[int] = None
#    DLGBR: Optional[int] = None
#    ULMBR: Optional[int] = None
#    DLMBR: Optional[int] = None
#    Protocol: Optional[str] = None
#    PassBlock: Optional[str] = None
#
## Define the ProductOrder model with all fields optional
#class ProductOrder(BaseModel):
#    id: Optional[str] = None
#    name: Optional[str] = None
#    administrative_state: Optional[str] = None
#    operational_state: Optional[str] = None
#    coverage_area: Optional[List[str]] = None
#    sst: Optional[int] = None
#    sd: Optional[str] = None
#    dnn: Optional[str] = None
#    prioritylabel: Optional[int] = None
#    uemobilitylevel: Optional[str] = None
#    reliability: Optional[float] = None
#    ulmaxpktsize: Optional[int] = None
#    dllatency: Optional[int] = None
#    ullatency: Optional[int] = None
#    delaytolerance: Optional[str] = None
#    dldeterministiccomm: Optional[str] = None
#    dldeterminperiodicity: Optional[int] = None
#    uldeterministiccomm: Optional[str] = None
#    uldeterminperiodicity: Optional[int] = None
#    dlguathptperue: Optional[int] = None
#    ulguathptperue: Optional[int] = None
#    dlmaxthptperue: Optional[int] = None
#    ulmaxthptperue: Optional[int] = None
#    dlguathptperslice: Optional[int] = None
#    ulguathptperslice: Optional[int] = None
#    dlmaxthptperslice: Optional[int] = None
#    ulmaxthptperslice: Optional[int] = None
#    termdensity: Optional[int] = None
#    maxnumberofpdusessions: Optional[int] = None
#    maxnumberofues: Optional[int] = None
#    n6protection: Optional[List[N6Protection]] = []
#    kpi: Optional[List[str]] = []
#
#class ProductOrderUE(BaseModel):
#    IMSI: int
#    numIMSIs: int 
#    slice: str 
#    IPV4: str
#    IPV6: str
#    AMDATA: bool
#    DEFAULT: str
#    UEcanSendSNSSAI: str
#    AMBRUP: Optional[int] = None
#    AMBRDW: Optional[int] = None



@app.post("/productOrder/post")
async def create_product_order(
    product_order: netslice_schemas.ProductOrder,
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


