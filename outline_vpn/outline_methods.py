from dotenv import load_dotenv
from outline_vpn.outline_vpn import OutlineVPN

import os


load_dotenv()

OUTLINE_API_URL = os.getenv('OUTLINE_API_URL')
CERT_SHA256 = os.getenv('CERT_SHA256')

# Setup the access with the API URL
# (Use the one provided to you after the server setup)
client = OutlineVPN(
    api_url=OUTLINE_API_URL,
    cert_sha256=CERT_SHA256
)


def get_all_keys(OUTLINE_API_URL, CERT_SHA256,):
    """Get all access URLs on the server."""
    keys = [('ID ключа', 'Имя ключа', 'Ключ')]
    for key in client.get_keys():
        keys.append((key.key_id, key.name, key.access_url))
    return keys


def create_new_key():
    """Create new key."""
    key_dict = {}
    # inputs for all fields of a new key
    # add it to dict than jsonify
    client.create_key(key_dict)


def rename_key(key_id, new_name):
    client.rename_key(key_id, new_name)


def delete_key(key_id):
    client.delete_key(key_id)


def add_data_limit(key_id, limit):
    """Set a monthly data limit int in MB"""
    client.add_data_limit(key_id, 1000 * 1000 * limit)


def remove_data_limit(key_id):
    """Remove the data limit."""
    client.delete_data_limit(key_id)


def get_key_by_id(key_id):
    """Show key before actions with it."""
    pass
