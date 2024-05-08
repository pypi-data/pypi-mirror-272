import subprocess
from flask import Flask, jsonify
import requests
import os
import schedule
import time
import sys


if len(sys.argv) != 4:
    print("Usage: python3 app.py <cname> <passkey>")
    sys.exit(1)


app = Flask(__name__)
app.secret_key = os.urandom(24)

#Parameters#######
new_ip = ""
old_ip = ""
protocol = ""
stack = sys.argv[1]
cname = sys.argv[2]
passkey = sys.argv[3]

interval = 90
#####################


def get_public_ip():
    global old_ip, new_ip, protocol
    
    if stack == '-4':
        try:
            result = subprocess.run(['curl', '-4', 'ifconfig.me'], capture_output=True, text=True)
            if result.returncode == 0:
                new_ip = result.stdout.strip()
                if new_ip != old_ip:
                    protocol = 'IPv4'
                    #print(new_ip)
                    return update_dns_record()
                    
        except Exception as e:
            return f"Error retrieving public IPv4: {e}"
        return new_ip
    
    elif stack == '-6':
        try:
            result = subprocess.run(['curl', '-6', 'ifconfig.me'], capture_output=True, text=True)
            if result.returncode == 0:
                new_ip = result.stdout.strip()
                if new_ip != old_ip:
                    protocol = 'IPv6'
                    #print(new_ip)
                    return update_dns_record()
                    
        except Exception as e:
            return f"Error retrieving public IPv6: {e}"
        return new_ip

    else:
        print("protocol not recognized! choose either '-4' for ipv4 or '-6' for ipv6 protocols respectively.")




@app.route('/update_ip', methods=['GET'])
def update_dns_record():
    global cname, old_ip, new_ip, passkey, protocol
    url = "https://ddns.dartfox.xyz/update_ip"

    payload = {
        "cname": cname,
        "passkey": passkey,
        "new_ip": new_ip,
        "protocol": protocol
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(response.text)
        old_ip = new_ip
        return response.text
    else:
        return response.text
    
# Function to perform IP check
schedule.every(interval).seconds.do(get_public_ip)

# Function to start scheduling
@app.route('/start', methods=['GET'])
def start_scheduling():
    global scheduling_running
    if not scheduling_running:
        scheduling_running = True
        print("Scheduling started...")
        while scheduling_running:
            schedule.run_pending()
            time.sleep(30)
        return jsonify({"message":"Scheduling started successfully."}), 200
    else:
        print("Scheduling is already running.")
        return jsonify({"message":"Scheduling is already running."}), 200


scheduling_running = False
start_scheduling()
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3030)
