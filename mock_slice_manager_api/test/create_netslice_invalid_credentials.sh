#!/bin/bash
# @Author: Rafael Direito
# @Date:   2025-06-21 10:11:03
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:18:17

# Credentials: admin:password -> Authorization: Basic YWRtaW46cGFzc3dvcmQ=
# Wrong Credentials: admin:admin -> Authorization: Basic YWRtaW46YWRtaW4=

curl --location --request POST '127.0.0.1:8000/productOrder/post' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46YWRtaW4=' \
--data '{
    "id": "5GASPHigh", 
    "name": "5gasp",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222222", 
    "dnn": "5gasp.eu", 
    "prioritylabel": 100, 
    "reliability": 99.9, 
    "dllatency": 20, 
    "ullatency": 20, 
    "delaytolerance": "NOT_SUPPORTED", 
    "dldeterministiccomm": "NOT_SUPPORTED", 
    "uldeterministiccomm": "NOT_SUPPORTED", 
    "ulguathptperue": 20000,
    "ulmaxthptperue": 50000,
    "dlguathptperue": 20000,
    "dlmaxthptperue": 50000,
    "n6protection":[{"type":"PCC Rule","name":"rule_any"}] 
}'