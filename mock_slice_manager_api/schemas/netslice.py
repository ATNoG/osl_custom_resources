# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:02:39
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 10:03:16
from pydantic import BaseModel
from typing import List, Optional

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