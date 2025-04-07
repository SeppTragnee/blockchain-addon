import requests
import json
import time
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
    """Laad de secrets uit een bestand."""
    with open(path, "r") as f:
        return json.load(f)

def get_sensor_value(sensor_id, ha_url, token):
    """Haal de waarde van de sensor op van Home Assistant."""
    url = f"{ha_url}/api/states/{sensor_id}"
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
    log("Certification gestart", "info")
    try:
        # Laad geheime gegevens
        secrets = load_secrets()

        # Haal sensorwaarde op
        sensor_id = secrets["sensor_id"]
        sensor_value = get_sensor_value(sensor_id, "http://localhost:8123", secrets["ha_token"])
        log(f"Sensorwaarde: {sensor_value} Wh", "info")

        # Genereer gecertificeerde string
        certified_string = generate_unique_certified_string(sensor_value)

        # Haal login hash op
        login_hash, username = get_login_hash(certified_string, secrets["blockchain_url"], secrets["address"])
        log(f"Login hash: {login_hash}", "info")

        # Onderteken de hash
        signed_hash = sign_hash(login_hash, secrets["blockchain_url"], secrets["private_key"])
        log(f"Signed hash: {signed_hash}", "info")

        # Certificeer de data
        result = certify_energy_data(username, signed_hash, certified_string, secrets["blockchain_url"])
        log(f"✓ Succesvol! transactionHash: {result.get('transactionHash')}", "success")

    except Exception as e:
        log(f"Fout: {e}", "error")
