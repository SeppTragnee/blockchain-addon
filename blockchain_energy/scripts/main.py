import requests
import json
import time
import os
from requests.auth import HTTPBasicAuth

def log(msg, level="info"):
    symbols = {
        "info": "[i]",
        "success": "[✓]",
        "warning": "[!]",
        "error": "[x]"
    }
    print(f"{symbols.get(level, '[ ]')} {msg}")

def get_sensor_value(sensor_id, ha_url, token):
    url = f"{ha_url}/api/states/{sensor_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()["state"]

def generate_unique_certified_string(sensor_value: str) -> str:
    timestamp_seconds = int(time.time())
    payload = {
        "data": f"smart_meter_Wh_{sensor_value}",
        "timestamp": timestamp_seconds
    }
    return json.dumps(payload)

def get_login_hash(message, blockchain_url, address):
    endpoint = f"{blockchain_url}/login?address={address}&message={message}"
    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()
    json_data = response.json()
    login_hash = json_data.get("hash")
    username = f'{json_data["address"]}/{json_data["timestamp"]}/{json_data["message"]}'
    return login_hash, username

def sign_hash(hash_value, blockchain_url, private_key):
    endpoint = f"{blockchain_url}/login/signMessage"
    payload = {"hash": hash_value, "key": private_key}
    response = requests.post(endpoint, json=payload, timeout=60)
    response.raise_for_status()
    return response.text.strip()

def certify_energy_data(username, password, certified_string, blockchain_url):
    endpoint = f"{blockchain_url}/certificationVerified/certify"
    payload = {
        "certifiedString": certified_string,
        "description": "Certified from Home Assistant"
    }
    response = requests.post(
        endpoint,
        json=payload,
        auth=HTTPBasicAuth(username, password),
        timeout=60
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    log("Certification gestart", "info")

    try:
        # 🔐 Gegevens ophalen uit omgevingsvariabelen (via shell_command)
        blockchain_url = os.environ.get("BLOCKCHAIN_URL")
        private_key = os.environ.get("PRIVATE_KEY")
        address = os.environ.get("ADDRESS")
        ha_token = os.environ.get("HA_TOKEN")
        sensor_id = os.environ.get("SENSOR_ID")
        ha_url = "http://localhost:8123"

        if not all([blockchain_url, private_key, address, ha_token, sensor_id]):
            raise ValueError("Niet alle vereiste omgevingsvariabelen zijn ingevuld.")

        # 📊 Stap 1: Sensor uitlezen
        sensor_value = get_sensor_value(sensor_id, ha_url, ha_token)
        log(f"Sensorwaarde: {sensor_value} Wh", "info")

        # 🧾 Stap 2: Unieke string aanmaken
        certified_string = generate_unique_certified_string(sensor_value)

        # 🔑 Stap 3: Login hash ophalen
        login_hash, username = get_login_hash(certified_string, blockchain_url, address)
        log(f"Login hash: {login_hash}", "info")

        # ✍️ Stap 4: Ondertekenen
        signed_hash = sign_hash(login_hash, blockchain_url, private_key)
        log(f"Signed hash: {signed_hash}", "info")

        # ✅ Stap 5: Certificeren
        result = certify_energy_data(username, signed_hash, certified_string, blockchain_url)
        log(f"✓ Succesvol! transactionHash: {result.get('transactionHash')}", "success")

    except Exception as e:
        log(f"Fout: {e}", "error")

