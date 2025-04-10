import requests
import json
import time
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth

def log(msg, level="info"):
    symbols = {
        "info": "[i]",
        "success": "[✓]",
        "warning": "[!]",
        "error": "[x]"
    }
    print(f"{symbols.get(level, '[ ]')} {msg}")

def load_secrets(path="/share/secrets.json"):
    """Load secrets from a file."""
    with open(path, "r") as f:
        return json.load(f)

def get_sensor_value(sensor_id):
    """Retrieve the value of the sensor using the internal Supervisor API."""
    token = os.environ.get("SUPERVISOR_TOKEN")
    url = f"http://supervisor/core/api/states/{sensor_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()["state"]

def generate_unique_certified_string(sensor_value: str) -> str:
    """Generate a certified string with timestamp and sensor value."""
    timestamp_seconds = int(time.time())
    payload = {
        "data": f"smart_meter_Wh_{sensor_value}",
        "timestamp": timestamp_seconds
    }
    return json.dumps(payload)

def get_login_hash(message, blockchain_url, address):
    """Request login hash from the blockchain API."""
    endpoint = f"{blockchain_url}/login?address={address}&message={message}"
    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()
    json_data = response.json()
    login_hash = json_data.get("hash")
    username = f'{json_data["address"]}/{json_data["timestamp"]}/{json_data["message"]}'
    return login_hash, username

def sign_hash(hash_value, blockchain_url, private_key):
    """Sign the login hash with the private key."""
    endpoint = f"{blockchain_url}/login/signMessage"
    payload = {"hash": hash_value, "key": private_key}
    response = requests.post(endpoint, json=payload, timeout=60)
    response.raise_for_status()
    return response.text.strip()

def certify_energy_data(username, password, certified_string, blockchain_url):
    """Certify the data using the blockchain API."""
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

def update_home_assistant_helpers(sensor_value, transaction_hash):
    """Update Home Assistant helpers with certified data."""
    token = os.environ.get("SUPERVISOR_TOKEN")
    ha_url = "http://supervisor/core/api/states"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Update certified energy value
    requests.post(
        f"{ha_url}/input_number.gecertificeerde_energie",
        headers=headers,
        json={"state": str(sensor_value)}
    )

    # 2. Save transaction hash
    requests.post(
        f"{ha_url}/input_text.certificatie_hash",
        headers=headers,
        json={"state": transaction_hash}
    )

    # 3. Set current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    requests.post(
        f"{ha_url}/input_datetime.laatste_certificatie",
        headers=headers,
        json={"state": timestamp}
    )

    log("Home Assistant helpers updated", "success")

if __name__ == "__main__":
    log("Certification process started", "info")
    try:
        # 1. Load secrets
        secrets = load_secrets()

        # 2. Retrieve sensor value
        sensor_value = get_sensor_value(secrets["sensor_id"])
        log(f"Sensor value: {sensor_value}", "info")

        # 3. Generate unique certified string
        certified_string = generate_unique_certified_string(sensor_value)

        # 4. Request login hash
        login_hash, username = get_login_hash(certified_string, secrets["blockchain_url"], secrets["address"])
        log(f"Login hash: {login_hash}", "info")

        # 5. Sign the hash
        signed_hash = sign_hash(login_hash, secrets["blockchain_url"], secrets["private_key"])
        log(f"Signed hash: {signed_hash}", "info")

        # 6. Certify the data
        result = certify_energy_data(username, signed_hash, certified_string, secrets["blockchain_url"])
        log(f"✓ Successfully certified! Transaction hash: {result.get('transactionHash')}", "success")

        # 7. Update Home Assistant helpers
        update_home_assistant_helpers(sensor_value, result.get("transactionHash"))

    except Exception as e:
        log(f"Error: {e}", "error")

