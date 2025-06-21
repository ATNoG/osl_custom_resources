# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-11 16:29:17
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:11:19
# Fully Generated with AI

from fastapi import FastAPI, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from typing import Optional
from fastapi.responses import JSONResponse
from auth.auth import authenticate
from schemas import netslice as netslice_schemas
from routers import (
    ue as ue_router,
    netslice as netslice_router
)
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
app.include_router(netslice_router.router, prefix="/productOrder", tags=["productOrder"])