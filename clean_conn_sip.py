#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from routeros_api import RouterOsApiPool
import sys
# import json
# RouterOS device details

if len(sys.argv) < 4:
    print("Informe o ip usuario senha respectivamente")
    sys.exit(1)

router_ip = sys.argv[1]
router_username = sys.argv[2]
router_password = sys.argv[3]

# Connect to the RouterOS device
api_pool = RouterOsApiPool(router_ip, username=router_username, password=router_password, plaintext_login=True)


try:
    api = api_pool.get_api()
except Exception as e:
    sys.stderr.write(f"Ocorreu um erro: {e}\n")
    sys.exit(1)

try:
    # Query firewall connections for SIP traffic
    sip_connections = api.get_resource('/ip/firewall/connection').get(
        **{"connection-type": "sip"})  # Adjust according to your SIP setup

    # Remove SIP-related connections
    for connection in sip_connections:
        api.get_resource('/ip/firewall/connection').remove(id=connection['id'])

    print("SIP connections removed successfully.")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Disconnect from RouterOS device
    api_pool.disconnect()
