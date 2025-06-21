#!/bin/bash
# @Author: Rafael Direito
# @Date:   2025-06-21 10:11:03
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 10:15:12

# Credentials: admin:password

curl --location --request POST '127.0.0.1:8080/UE/post' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' \
--data '{
    "IMSI": 1, 
    "numIMSIs":2, 
    "slice": "second_slice", 
    "IPV4": "", 
    "IPV6": "", 
    "AMDATA": true,
    "DEFAULT": "TRUE",
    "UEcanSendSNSSAI": "TRUE",
    "AMBRUP": 2000000,  
    "AMBRDW": 2000000   
}'