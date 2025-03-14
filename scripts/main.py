import requests
import json
import os
import time

# Blockchain API details
BLOCKCHAIN_API_URL = "http://84.88.154.234:3000"
PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "your_private_key_here")
ADDRESS = "0xbb678ed4adb678bad4b8f7203135ae1854463a7f"

# Home Assistant API details
HA_API_URL = "http://supervisor/core/api/states/sensor.smart_meter_63a_energia_real_consumida"
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
    "Content-Type": "application/json"
}

def get_energy_usage():
    """Fetch energy usage data from Home Assistant sensor."""
    try:
        response = requests.get(HA_API_URL, headers=HEADERS)
        data = response.json()
        return data.get("state", "0")
    except Exception as e:
        print(f"Error fetching energy data: {e}")
        return None

def certify_to_blockchain(energy_data):
    """Send certified energy data to the blockchain."""
    payload = {
        "private_key": PRIVATE_KEY,
        "address": ADDRESS,
        "data": energy_data
    }
    try:
        response = requests.post(f"{BLOCKCHAIN_API_URL}/certify", json=payload)
        print(f"Blockchain Response: {response.text}")
    except Exception as e:
        print(f"Error sending data to blockchain: {e}")

if __name__ == "__main__":
    while True:
        energy_data = get_energy_usage()
        if energy_data:
            print(f"Energy Data: {energy_data} kWh")
            certify_to_blockchain(energy_data)
        time.sleep(60)  # Certify every 60 seconds
