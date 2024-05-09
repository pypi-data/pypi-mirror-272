from bradescoPixCTS.statusCode import *
import requests
import sys
import json


class RequestApi:

    def __init__(self, uri, method, access_token, cert, payload=None):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "connect_timeout": "5",
            "timeout": "15",
            # "http_errors" : False,
        }

        if method == "GET":
            response = requests.get(uri, headers=headers, cert=cert)
        elif method == "POST":
            response = requests.post(uri, json=payload, headers=headers, cert=cert)
        elif method == "PUT":
            response = requests.put(uri, json=payload, headers=headers, cert=cert)
        elif method == "DELETE":
            response = requests.delete(uri, headers=headers, cert=cert)
        else:
            raise ValueError("Invalid HTTP method.")

        try:
            response_data = response.json()

            # set statusDescription
            function_name = sys._getframe(1).f_code.co_name
            statusDetail = getattr(StatusCode(), function_name, None)
            if statusDetail:
                status = response_data["status"] if "status" in response_data else None
                response_data["statusDescription"] = statusDetail(
                    response.status_code, status
                )
            else:
                response_data["statusDescription"] = None

        except ValueError as e:
            response_data = response
        
        self.response = response_data
