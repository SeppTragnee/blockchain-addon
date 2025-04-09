import requests
import json
import time
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Locatie van het logbestand in Home Assistant
LOG_PATH = "/config/www/log_certificatie.txt"

def log(msg, level="info"):
    symbols = {
        "info": "[i]",
        "success": "[✓]",
        "warning": "[!]",
        "error": "[x]"
    }
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"{timestamp} {symbols.get(level, '[ ]')} {msg}"

    # Print naar terminal
    print(formatted)

    # Append naar logbestand
    try:
        with open(LOG_PATH, "a") as f:
            f.write(formatted + "\n")
    except Exception as file_error:
        print(f"[!] Kon log niet wegschrijven: {file_error}")

def load_secrets(path="/share/secrets.json"):
    """Laad de secrets uit een bestand."""
    with open(path, "r") as f:
        return json.load(f)

def get_sensor_value(sensor_id):
    """Haal de waarde van de sensor op via de interne Supervisor API."""
    token = os.environ.get("SUPERVISOR_TOKEN")
    print(token)
    
    url = f"http://supervisor/core/api/states/{sensor_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()["state"]

def generate_unique_certified_string(sensor_value: str) -> str:
    """Genereer een gecertificeerde string met een timestamp en sensorwaarde."""
    timestamp_seconds = int(time.time())
    payload = {
        "data": f"smart_meter_Wh_{sensor_value}",
        "timestamp": timestamp_seconds
    }
    return json.dumps(payload)

def get_login_hash(message, blockchain_url, address):
    """Vraag de login hash aan bij de blockchain API."""
    endpoint = f"{blockchain_url}/login?address={address}&message={message}"
    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()
    json_data = response.json()
    login_hash = json_data.get("hash")
    username = f'{json_data["address"]}/{json_data["timestamp"]}/{json_data["message"]}'
    return login_hash, username

def sign_hash(hash_value, blockchain_url, private_key):
    """Onderteken de login hash met de private key."""
    endpoint = f"{blockchain_url}/login/signMessage"
    payload = {"hash": hash_value, "key": private_key}
    response = requests.post(endpoint, json=payload, timeout=60)
    response.raise_for_status()
    return response.text.strip()

def certify_energy_data(username, password, certified_string, blockchain_url):
    """Certificeer de data met de blockchain API."""
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
    log("Certificatie gestart", "info")
    try:
        # Laad secrets (zonder ha_token)
        secrets = load_secrets()

        # Haal sensorwaarde op via interne API met SUPERVISOR_TOKEN
        sensor_value = get_sensor_value(secrets["sensor_id"])
        log(f"Sensorwaarde: {sensor_value}", "info")

        # Genereer string
        certified_string = generate_unique_certified_string(sensor_value)

        # Login hash ophalen
        login_hash, username = get_login_hash(certified_string, secrets["blockchain_url"], secrets["address"])
        log(f"Login hash: {login_hash}", "info")

        # Onderteken de hash
        signed_hash = sign_hash(login_hash, secrets["blockchain_url"], secrets["private_key"])
        log(f"Signed hash: {signed_hash}", "info")

        # Certificeer de data
        result = certify_energy_data(username, signed_hash, certified_string, secrets["blockchain_url"])
        log(f"✓ Succesvol gecertificeerd! Transaction hash: {result.get('transactionHash')}", "success")

    except Exception as e:
        log(f"Fout: {e}", "error")
