# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:02:51
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 10:03:37
from pydantic import BaseModel
from typing import List, Optional

class UE(BaseModel):
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