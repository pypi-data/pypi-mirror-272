import requests
import base64


class AccessToken:

    def __init__(
        self, client_id, client_secret, public_key_path, private_key_path, environment
    ):

        self.sandbox = environment.sandbox
        self.cert = (public_key_path, private_key_path)
        credential = f"{client_id}:{client_secret}"
        credential_base64 = base64.b64encode(credential.encode()).decode()

        headers = {
            "Authorization": f"Basic {credential_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        param = {"grant_type": "client_credentials"}

        response = requests.post(
            environment.url_token, headers=headers, data=param, cert=self.cert
        )

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.token_type = token_data.get("token_type")
            self.expires_in = token_data.get("expires_in")

        else:
            self.error = (
                f"Error - Access Token: {response.status_code} - {response.text}"
            )
