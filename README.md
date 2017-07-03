# HalfCaff
OSX Status Bar app to keep laptop from sleeping when Cisco VPN is connected

The Cisco Anyconnect VPN app with RSA token authentication has a problem. 
It does not change the sleep setting on OSX when connected and as a result, when the machine sleeps
VPN is disconnected. This can be a real pain with the 2FA token.

There are plenty of tools (Cafeine, caffeinate, etc) which will work on the commandline or provide a nice status bar
for setting the amount of time to keep the system awake for. This was an excuse to learn some new tools and accessing Coacoa
from Python. The end result is more useful to me than all the other tools.

The statusbar will detect when a VPN connection is active, and it will provide the option to keep the system from entering
idle (but will still have hte screen turn timeout and lock.) There are options to 'auto-enable' the sleep prevention on VPN
conneciton, and starting HalfCaff on login. Options are presistent and stored in 
~/Library/Application Support/HalfCaff/options.json

There are two hidden options only available in the json file, the vpn client path, and the polling inerval:

```json
{"vpncli": "/opt/cisco/anyconnect/bin/vpn", 
 "monitor_interval": 150, 
 "auto_caffeinate": false}
```

