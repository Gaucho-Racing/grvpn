from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from urllib.parse import parse_qs, urlparse
import os
import json
import requests

OAUTH_PORT = 10315
SENTINEL_CLIENT_ID = "aLrhpakeWRop"
SENTINEL_CLIENT_SECRET = "ms44tvgxg2DBaZtX3VfhAbB6FumGuYRY"
SENTINEL_REDIRECT_URI = f"http://localhost:{OAUTH_PORT}/auth/callback"
SENTINEL_AUTH_URL = f"https://sso.gauchoracing.com/oauth/authorize?client_id={SENTINEL_CLIENT_ID}&redirect_uri={SENTINEL_REDIRECT_URI}&response_type=code&scope=user:read&prompt=none"

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/auth/callback":
            params = parse_qs(parsed_url.query)
            code = params.get("code", [None])[0]
            success_file_path = os.path.join(os.path.dirname(__file__), "static", "success.html")
            try:
                with open(success_file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Login successful. You may close this window.</h1></body></html>")

            token = Sentinel.exchange_code(code)
            if token.get("access_token"):
                Sentinel.save_credentials(token)

            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

class Sentinel:

    @staticmethod
    def verify_credentials():
        credentials = Sentinel.get_saved_credentials()
        if not credentials:
            return False
        user_info = Sentinel.get_user_info()
        if not user_info:
            # Try to refresh credentials
            credentials = Sentinel.refresh_credentials()
            if not credentials:
                return False
            Sentinel.save_credentials(credentials)
            user_info = Sentinel.get_user_info()
            if not user_info:
                return False
        return True

    @staticmethod
    def get_saved_credentials():
        app_dir = os.path.expanduser("~/.grvpn")
        credentials_file = os.path.join(app_dir, "credentials.json")

        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as file:
                credentials = json.load(file)
            return credentials
        else:
            return None
    
    @staticmethod
    def save_credentials(credentials: dict):
        app_dir = os.path.expanduser("~/.grvpn")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        credentials_file = os.path.join(app_dir, "credentials.json")
        with open(credentials_file, 'w') as file:
            json.dump(credentials, file)

    @staticmethod
    def run_auth_server():
        httpd = HTTPServer(("localhost", OAUTH_PORT), OAuthHandler)
        httpd.serve_forever()
        
    @staticmethod   
    def exchange_code(code: str):
        response = requests.post(f"https://vpn.gauchoracing.com/api/auth/login?code={code}")
        return response.json()
    
    @staticmethod
    def refresh_credentials():
        credentials = Sentinel.get_saved_credentials()
        if not credentials:
            return None
        response = requests.post(f"https://sso.gauchoracing.com/api/oauth/token", data={
            "grant_type": "refresh_token",
            "refresh_token": credentials["refresh_token"],
            "client_id": SENTINEL_CLIENT_ID,
            "client_secret": SENTINEL_CLIENT_SECRET,
            "redirect_uri": SENTINEL_REDIRECT_URI
        })
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def get_user_info():
        credentials = Sentinel.get_saved_credentials()
        if not credentials:
            return None
        response = requests.get(f"https://vpn.gauchoracing.com/api/users/@me", headers={"Authorization": f"Bearer {credentials['access_token']}"})
        return response.json() if response.status_code == 200 else None