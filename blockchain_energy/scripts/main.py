import requests
import json
import os
import time

BLOCKCHAIN_API_URL = "http://84.88.154.234:3000"
PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "your_private_key_here")
ADDRESS = "0xbb678ed4adb678bad4b8f7203135ae1854463a7f"

HA_API_URL = "http://supervisor/core/api/states/sensor.smart_meter_63a_energia_real_consumida"
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
    "Content-Type": "application/json"
}

def get_energy_usage():
    try:
        response = requests.get(HA_API_URL, headers=HEADERS)
        print(f"HA response status: {response.status_code}")  # Duidelijker
        data = response.json()
        energy_state = data.get("state", None)
        print(f"Energie state ontvangen: {energy_state}")
        return energy_state
    except Exception as e:
        print(f"Error fetching energy data: {e}")
        return None

def certify_to_blockchain(energy_data):
    payload = {
        "private_key": PRIVATE_KEY,
        "address": ADDRESS,
        "data": energy_data
    }
    try:
        response = requests.post(f"{BLOCKCHAIN_API_URL}/certify", json=payload)
        print(f"Blockchain Response [{response.status_code}]: {response.text}")
    except Exception as e:
        print(f"Error sending data to blockchain: {e}")

if __name__ == "__main__":
    print("==> Script gestart")
    while True:
        energy_data = get_energy_usage()
        if energy_data:
            print(f"Energy Data: {energy_data} kWh - verzenden naar blockchain...")
            certify_to_blockchain(energy_data)
        else:
            print("Geen energiedata ontvangen, controleer sensor en token.")
        time.sleep(60)
