# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 11:11:02
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:04:02
from enum import Enum

class UEMode(str, Enum):
    Implicit = "IMPLICIT"
    Explicit = "EXPLICIT"

class UEType(str, Enum):
    ReRegister_NotRequired = "REREG_NOTREQ"
    ReRegister_Required = "REREG_REQ"

class UECause(str, Enum):
    Custom = "CUSTOMER_DEF"
    IllegalUE = "ILLEGAL_UE"
    IllegalME = "ILLEGAL_ME"
    ServerNotAllowed = "SRV_NOT_ALLOW"
    PLMNNotAllowed = "PLMN_NOT_ALLOW"
    TrackingAreaNotAllowed = "AREA_NOT_ALLOW"
    RoamNotAllowed = "ROAM_NOT_ALLOW"
    N1NotAllowed = "N1_NOT_ALLOW"
    PeiNotAccepted = "PEI_NOT_ALLOW"
    UECannotBeDerived = "UE_UN_DERIVED"
    ImplicitDeRegistered = "IMPLICIT_DEREG"
    NoSuitableCellsInTrackingArea = "NO_CELL_IN_TA"
    Non3GPPNotAllowed = "NON_3GPP_NOT_ALLOW"

class CNThptUnit(str, Enum):
    bps = "bps"
    Kbps = "Kbps"
    Mbps = "Mbps"
    Gbps = "Gbps"
    Tbps = "Tbps"

class CNHighLatencyCommBuffer(str, Enum):
    NoHLC = "NOT_REQUESTED"
    HLCNoBuffer = "NO_SUGGESTED"
    HLCBuffer = "REQUESTED"
    
class CNPDUtype(str, Enum):
    IPV4V6 = "IPV4V6"
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    UNSTR = "UNSTR"
    ETHER = "ETHER"
    
    def __str__(self):
        return str(self.value)

class CNSSCMode(str, Enum):
    SSC_MODE_1 = "SSC_MODE_1"
    SSC_MODE_2 = "SSC_MODE_2"
    SSC_MODE_3 = "SSC_MODE_3"
    
class CNProtection(str, Enum):
    NOT_NEEDED = "NOT_NEEDED"
    REQUIRED = "REQUIRED"
    PREFERED = "PREFERED"

class CNIPTYPE(str, Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"

class CNProtocolType(str, Enum):
    ANY = "ANY" 
    GRE = "GRE" 
    ICMP = "ICMP"
    TCP = "TCP"
    UDP = "UDP"

    def default():
        return CNProtocolType.ANY

class CNPassBlock(str, Enum):
    PASS = "pcc_action_pass" 
    BLOCK = "pcc_action_block"
    UE = "ue_initiated"
    SERVER = "server_initiated"
    
class CNNetFunction(str, Enum):
    SMF="NfSMF"
    AMF="NfAMF"

class CNEnableDisable(str, Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"

class CNDefaultSpecific(str, Enum):
    DEFAULT = "DEFAULT"
    SPECIFIC = "SPECIFIC"

class CustomBoolean(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    
class uEmobilityLevel(str, Enum):
    stationary = "stationary"
    nomadic = "nomadic"
    restricted_mobility = "restricted_mobility"
    fully_mobility = "fully_mobility"

class synchonicity(str, Enum):
    NOT_SUPPORTED = "NOT_SUPPORTED"
    BETWEEN_BS_AND_UE = "BETWEEN_BS_AND_UE"
    Between_BS_and_UE_and_UE = "BETWEEN_BS_AND_UE_&_UE_AND_UE"

class positioning(str, Enum):
    CIDE_CID = "CIDE_CID"
    OTDOA = "OTDOA"
    RF_fingerprint = "RF_fingerprint"
    AECID = "AECID"
    Hybrid_positioning = "Hybrid_positioning"
    NET_RTK = "NET_RTK"

    
class positioningfreq(str, Enum):
    PERSEC="PERSEC"
    PERMIN="PERMIN"
    PERHOUR="PERHOUR"

class sliceuse(str, Enum):
    ZERO="0"   #any slice
    ONE="1"    #slices with same SST
    TWO="2"    #slices with same SD
    THREE="3"  #no other slice
    FOUR="4"   #restricted locations
    
class energyKPI(str, Enum):
    eMBBEEPerfReq = "eMBBEEPerfReq"
    uRLLCEEPerfReq = "uRLLCEEPerfReq"
    mIoTEEPerfReq = "mIoTEEPerfReq"

class sharing(str, Enum):
    shared="shared"
    non_shared="non_shared"

class nssaa(str, Enum):
    SUPPORTED="SUPPORTED"
    NOT_SUPPORTED="NOT_SUPPORTED"

class usermgmt(str, Enum):
    SUPPORTED="SUPPORTED"
    NOT_SUPPORTED="NOT_SUPPORTED"

class NBIoT(str, Enum):
    SUPPORTED="SUPPORTED"
    NOT_SUPPORTED="NOT_SUPPORTED"

class DeterministicCommAvailability(str, Enum):
    SUPPORTED="SUPPORTED"
    NOT_SUPPORTED="NOT_SUPPORTED"

class DelayTolerance(str, Enum):
    SUPPORTED="SUPPORTED"
    NOT_SUPPORTED="NOT_SUPPORTED"

class V2XMode(str, Enum):
    SUPPORTED_BY_NR="SUPPORTED_BY_NR"
    NOT_SUPPORTED="NOT_SUPPORTED"
    
class AdministrativeState(str, Enum):
    LOCKED="LOCKED"
    UNLOCKED="UNLOCKED"
    SHUTTINGDOWN="SHUTTINGDOWN"
    
class OperationalState(str, Enum):
    ENABLED="ENABLED"
    DISABLED="DISABLED"