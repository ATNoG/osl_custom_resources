# Fully Generated with AI

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse

app = FastAPI()

# Define the N6Protection model with additional optional fields
class N6Protection(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    priority: Optional[int] = None
    ServerIP: Optional[str] = None
    MaskLen: Optional[int] = None
    startport: Optional[int] = None
    endport: Optional[int] = None
    ULGBR: Optional[int] = None
    DLGBR: Optional[int] = None
    ULMBR: Optional[int] = None
    DLMBR: Optional[int] = None
    Protocol: Optional[str] = None
    PassBlock: Optional[str] = None

# Define the ProductOrder model with all fields optional
class ProductOrder(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    administrative_state: Optional[str] = None
    operational_state: Optional[str] = None
    coverage_area: Optional[List[str]] = None
    sst: Optional[int] = None
    sd: Optional[str] = None
    dnn: Optional[str] = None
    prioritylabel: Optional[int] = None
    uemobilitylevel: Optional[str] = None
    reliability: Optional[float] = None
    ulmaxpktsize: Optional[int] = None
    dllatency: Optional[int] = None
    ullatency: Optional[int] = None
    delaytolerance: Optional[str] = None
    dldeterministiccomm: Optional[str] = None
    dldeterminperiodicity: Optional[int] = None
    uldeterministiccomm: Optional[str] = None
    uldeterminperiodicity: Optional[int] = None
    dlguathptperue: Optional[int] = None
    ulguathptperue: Optional[int] = None
    dlmaxthptperue: Optional[int] = None
    ulmaxthptperue: Optional[int] = None
    dlguathptperslice: Optional[int] = None
    ulguathptperslice: Optional[int] = None
    dlmaxthptperslice: Optional[int] = None
    ulmaxthptperslice: Optional[int] = None
    termdensity: Optional[int] = None
    maxnumberofpdusessions: Optional[int] = None
    maxnumberofues: Optional[int] = None
    n6protection: Optional[List[N6Protection]] = []
    kpi: Optional[List[str]] = []

class ProductOrderUE(BaseModel):
    IMSI: int
    numIMSIs: int 
    slice: str 
    IPV4: str
    IPV6: str
    AMDATA: bool
    DEFAULT: str
    UEcanSendSNSSAI: str
    AMBRUP: Optional[int] = None
    AMBRDW: Optional[int] = None



@app.post("/productOrder/post")
async def create_product_order(
    product_order: ProductOrder,
    authorization: Optional[str] = Header(None)
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


@app.post("/UE/post")
async def create_ue(
    ue: ProductOrderUE,
    authorization: Optional[str] = Header(None)
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
