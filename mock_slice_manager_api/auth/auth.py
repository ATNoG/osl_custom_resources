# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 09:52:49
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 10:01:04

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from aux.constants import AUTH_USERNAME, AUTH_PASSWORD

security = HTTPBasic()

def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    if creds.username != AUTH_USERNAME or creds.password != AUTH_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return creds