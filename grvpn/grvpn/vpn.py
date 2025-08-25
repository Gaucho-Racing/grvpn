from datetime import datetime, timezone
import os
import json
import requests

from grvpn.auth import Sentinel

class VPN:

    @staticmethod
    def test_connection():
        try:
            response = requests.get("https://vpn.gauchoracing.com/api/test", timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return None

    @staticmethod
    def get_profile():
        app_dir = os.path.expanduser("~/.grvpn")
        ovpn_files = [f for f in os.listdir(app_dir) if f.endswith('.ovpn')]
        if ovpn_files:
            return os.path.join(app_dir, ovpn_files[0])
        else:
            return None
        
    @staticmethod
    def save_profile(client_id: str, profile_text: str):
        app_dir = os.path.expanduser("~/.grvpn")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        for file in os.listdir(app_dir):
            if file.endswith('.ovpn'):
                os.remove(os.path.join(app_dir, file))
        with open(os.path.join(app_dir, f"{client_id}.ovpn"), "w") as f:
            f.write(profile_text)
        
    @staticmethod
    def get_client_info(id: str):
        credentials = Sentinel.get_saved_credentials()
        if not credentials:
            return None
        response = requests.get(f"https://vpn.gauchoracing.com/api/clients/{id}", headers={"Authorization": f"Bearer {credentials['access_token']}"})
        return response.json() if response.status_code == 200 else None
    
    @staticmethod
    def new_client():
        credentials = Sentinel.get_saved_credentials()
        if not credentials:
            return None
        response = requests.post(
            f"https://vpn.gauchoracing.com/api/clients",
            headers={"Authorization": f"Bearer {credentials['access_token']}"},
            json={
                "user_id": Sentinel.get_user_info()["id"],
                "profile_text": "",
                "profile_location": "",
                "expires_at": datetime.now(timezone.utc).isoformat()[:19] + "Z",
                "created_at": datetime.now(timezone.utc).isoformat()[:19] + "Z",
            }
        )
        return response.json() if response.status_code == 200 else None