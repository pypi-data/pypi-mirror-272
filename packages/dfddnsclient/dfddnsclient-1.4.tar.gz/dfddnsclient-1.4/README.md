#COMMAND LINES:

FOR LINUX/MACOS:

python3 -m venv dfddnsclient

source dfddnsclient/bin/activate

pip3 install dfddnsclient

#Activating dartfox ddns client for IPv4...
dfddnsclient -4 <your-cname> <your-pass-key>

#Activating dartfox ddns client for IPv6...
dfddnsclient -6 <your-cname> <your-pass-key>

#

#

#

#

FOR WINDOWS:

python -m venv dfddnsclient

source dfddnsclient/bin/activate

pip install dfddnsclient

#Activating dartfox ddns client for IPv4...
dfddnsclient -4 <your-cname> <your-pass-key>

#Activating dartfox ddns client for IPv6...
dfddnsclient -6 <your-cname> <your-pass-key>
