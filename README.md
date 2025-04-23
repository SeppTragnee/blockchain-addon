# Energy Certification via Blockchain for Home Assistant

This module is part of a bachelor project developed during an internship at the eXiT research group at the Universitat de Girona. The goal is to explore how blockchain technology can improve the security and trustworthiness of energy data in smart home environments using Home Assistant.

## 🌍 Project Overview

Modern smart homes rely on platforms like [Home Assistant](https://www.home-assistant.io/) to manage and automate devices such as energy meters and solar panels. However, as energy management becomes increasingly critical — especially for audits, taxation, and energy efficiency reports — the reliability and authenticity of sensor data becomes equally important.

This module introduces a blockchain-based solution to **certify energy usage data** securely and immutably, ensuring that once data is logged, it cannot be tampered with.

## 🔐 Why Blockchain?

Blockchain is a decentralized technology that stores data in an immutable chain of blocks. By leveraging blockchain, this module allows sensor data from Home Assistant to be:
- ✅ Authenticated
- 🔒 Immutable
- 📄 Traceable
- 🌐 Verifiable by external parties

This adds a layer of trust that is especially valuable for audits and regulatory reporting.

## ⚙️ How It Works

1. **Energy Data Collection**: Home Assistant reads real-time energy usage from smart meters.
2. **Hashing**: The sensor value is hashed using a secure algorithm.
3. **Signing**: The hash is signed with a private key for authenticity.
4. **Blockchain Certification**: The signed data is sent to a blockchain endpoint where it is recorded immutably.

## 📦 Module Setup

This module can be integrated into Home Assistant using external shell scripts and API calls. It is designed for flexibility and modularity.

### Requirements
- Python 3.10+
- Home Assistant (tested locally on Raspberry Pi)
- Blockchain endpoint (e.g., testnet or local validator)
- `secrets.yaml` for storing sensitive values like private keys and tokens

