import re
import delegator

# [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]
# /opt/cisco/anyconnect/bin/vpn state
"""
$ /opt/cisco/anyconnect/bin/vpn state
Cisco AnyConnect Secure Mobility Client (version 4.1.06020) .

Copyright (c) 2004 - 2015 Cisco Systems, Inc.  All Rights Reserved.


  >> state: Disconnected
  >> state: Disconnected
  >> state: Disconnected
  >> notice: Ready to connect.
  >> registered with local VPN subsystem.
VPN> 

"""

_re_connected = re.compile('  >> state: Connected')

def connected(vpncli):
    vpn = delegator.run(vpncli + ' state')
    found = _re_connected.findall(vpn.out)
    return bool(found)
