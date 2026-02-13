
import requests
import json
import urllib3
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://localhost:8443/nifi-api"
USERNAME = "admin"
PASSWORD = "ShopVerseAnalytics2026!"
TEMPLATE_FILE = "nifi_flow.json"

def get_token():
    print("[Auth] Authenticating...")
    resp = requests.post(
        f"{BASE_URL}/access/token",
        data={"username": USERNAME, "password": PASSWORD},
        verify=False
    )
    if resp.status_code == 201:
        return resp.text
    else:
        print(f"[Error] Auth Failed: {resp.text}")
        exit(1)

def get_root_pg(token):
    print("[Info] Finding Root Process Group...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/flow/process-groups/root", headers=headers, verify=False)
    return resp.json()["processGroupFlow"]["id"]

def upload_process_group(token, parent_pg_id):
    print(f"[Info] Uploading Process Group to [{parent_pg_id}]...")
    headers = {"Authorization": f"Bearer {token}"}
    files = {
        'file': ('nifi_flow.json', open(TEMPLATE_FILE, 'rb'), 'application/json')
    }
    
    url = f"{BASE_URL}/process-groups/{parent_pg_id}/process-groups/upload"
    

    data = {
        'groupName': 'ShopVerse Analytics',
        'positionX': 0,
        'positionY': 0,
        'clientId': 'deploy-script-v1'
    }
    
    resp = requests.post(url, headers=headers, files=files, data=data, verify=False)
    
    if resp.status_code == 201:
        print("[OK] Process Group Uploaded & Instantiated!")
        return True
    else:
        print(f"[Error] Upload Failed: {resp.status_code} - {resp.text}")
        return False

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"[Error] File not found: {TEMPLATE_FILE}")
        return

    try:
        token = get_token()
        root_pg = get_root_pg(token)
        upload_process_group(token, root_pg)
    except Exception as e:
        print(f"[Error] Script Error: {e}")

if __name__ == "__main__":
    main()
