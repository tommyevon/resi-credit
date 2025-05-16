import requests
from base64 import b64encode


class FannieMae:

    url = "https://api.fanniemae.com"

    def _get_bearer_token(self):
        """
        Get a bearer token for the Fannie Mae API.
        """
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = b64encode(auth_str.encode()).decode()

        url = "https://auth.pingone.com/4c2b23f9-52b1-4f8f-aa1f-1d477590770c/as/token"
        headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Content-type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    
    def _get_request(self, url_ext: str):
        """
        Make a GET request to the Fannie Mae API.
        """
        headers = {
            "Content-Type": "application/json",
            "x-public-access-token": self._get_bearer_token()
        }
        req = requests.get(self.url + url_ext, headers=headers)
        if req.status_code == 200:
            return req.json()
        else:
            raise Exception(f"Error: {req.status_code} - {req.text}")

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_econ(self, indicator: str):
        return self._get_request(f"/v1/economic-forecasts/indicators/{indicator}")

    def get_crt(self, historical: bool = True):
        if historical:
            url_ext = "/v1/connecticut-ave-securities/program-to-date"
        else:
            url_ext = "/v1/connecticut-ave-securities/current-reporting-period"

        return self._get_request(url_ext)
