from commonData import THINGSBOARD_HOST
import requests

class RestClient:
    def __init__(self, base_url=THINGSBOARD_HOST):
        self.base_url = base_url
        self.token = None
        self.headers = {}
    
    def login(self, username, password):
        payload = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/api/auth/login", json=payload)
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.headers = {"X-Authorization": f"Bearer {self.token}"}
            return True
        return False
    
    def get_user(self):
        return requests.get(f"{self.base_url}/api/auth/user", headers=self.headers).json()
    
    def get_allowed_permissions(self):
        return requests.get(f"{self.base_url}/api/user/permission", headers=self.headers).json()
    
    def get_user_dashboards(self, page_size=10, page=0):
        return requests.get(f"{self.base_url}/api/user/dashboards?pageSize={page_size}&page={page}", 
                           headers=self.headers).json()
    
    def get_device_telemetry(self, device_id, keys):
        keys_param = ",".join(keys)
        return requests.get(
            f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys={keys_param}", 
            headers=self.headers).json()
    
    def get_devices(self, page_size=100, page=0):
        return requests.get(
            f"{self.base_url}/api/tenant/devices?pageSize={page_size}&page={page}", 
            headers=self.headers).json()
    
    def get_user_role(self, user_id):
        try:
            return requests.get(f"{self.base_url}/api/user/{user_id}/authority", headers=self.headers).json()
        except Exception as e:
            print(f"Error getting user role: {str(e)}")
            return {"name": "Unknown"}