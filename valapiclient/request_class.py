import requests
import json
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class Request:
    def __init__(self, url, access_token=None, session=None):
        self.session = session if session else requests.Session()
        self.session.verify = False  # Ensure SSL verification is disabled
        self.url = url

        if access_token:
            self.session.headers.update(access_token)

    def get_json(self):
        response = self.session.get(self.url)

        # Log response status and content for debugging
        print(f"Request URL: {self.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")  # This will help you see what's coming back

        # Check if the response is empty
        if response.status_code == 200 and response.text.strip():  # Ensure the response is not empty
            try:
                return response.json()  # Parse JSON if available
            except ValueError:
                print("Error: Response is not valid JSON.")
                return None  # Handle the case where the response isn't valid JSON
        else:
            print(f"Error: Unexpected status code {response.status_code} or empty response.")
            return None  # Return None if the response is empty or the status code is not 200

    def post(self, value=None):
        if value:
            return self.session.post(self.url, json=value).status_code
        return self.session.post(self.url).status_code

    def put(self, value):
        return self.session.put(self.url, json=value).status_code

    def delete(self, value=None):
        return self.session.delete(self.url, json=value).status_code
