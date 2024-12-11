import requests
import base64
import json
import ssl
import re
import os
from os import path
import time

from pythonping import ping
from urllib3.exceptions import InsecureRequestWarning
from .request_class import Request

from .endpoints import (
    CoreGameEndpoints,
    LocalEndpoints,
    PartyEndpoints,
    PreGameEndpoints,
    PvPEndpoints,
    SessionsEndpoints,
    StoreEndpoints,
)

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class TLSAdapter(requests.adapters.HTTPAdapter):
    FORCED_CIPHERS = [
        'ECDHE-ECDSA-AES128-GCM-SHA256',
        'ECDHE-ECDSA-CHACHA20-POLY1305',
        'ECDHE-RSA-AES128-GCM-SHA256',
        'ECDHE-RSA-CHACHA20-POLY1305',
        'ECDHE+AES128',
        'RSA+AES128',
        'ECDHE+AES256',
        'RSA+AES256',
        'ECDHE+3DES',
        'RSA+3DES'
    ]

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.set_ciphers(':'.join(self.FORCED_CIPHERS))
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

def gen_pvp_base_url(prefix="pd", region="eu"):
    return f"https://{prefix}.{region}.a.pvp.net/"

class ValClient:
    def __init__(self, ip, port, username, password):
        self.base_url = f"https://{ip}:{port}/"
        self.pvp_base_url = gen_pvp_base_url()
        self.auth_token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("utf-8")
        self.local_header = {'Authorization': f"Basic {self.auth_token}"}

        self.session = requests.Session()

        self.local_session = requests.Session()
        self.local_session.verify = False
        self.local_session.headers.update(self.local_header)

        # Obtain clientVersion and clientPlatform
        self.client_version = self.get_current_version()
        self.client_platform = self.get_client_platform()

        # Authenticate and set up the headers
        self.auth_headers = self.get_auth_headers()
        self.base_pvp_header = self.auth_headers

        # Initialize endpoint classes
        self.coregame = CoreGameEndpoints(self)
        self.local = LocalEndpoints(self)
        self.party = PartyEndpoints(self)
        self.pregame = PreGameEndpoints(self)
        self.pvp = PvPEndpoints(self)
        self.sessions = SessionsEndpoints(self)
        self.store = StoreEndpoints(self)

        try:
            self.region = self.get_region()
        except Exception as e:
            print(f"Error getting region: {e}, using default 'eu'.")
            self.region = "eu"

            # Now initialize pvp_base_url using the correct region
        self.pvp_base_url = f"https://pd.{self.region}.a.pvp.net"

        # Initialize other base URLs
        self.glz_base_url = f"https://glz-{self.region}-1.{self.region}.a.pvp.net"
        self.shared_base_url = f"https://shared.{self.region}.a.pvp.net"

    def get_glz_url(self):
        return f"https://glz-{self.region}-1.{self.region}.a.pvp.net"

    def get_shared_url(self):
        return f"https://shared.{self.region}.a.pvp.net"

    def get_pd_url(self):
        return f"https://pd.{self.region}.a.pvp.net"

    def handle_local_request(self, suffix, method="GET", json_data=None):
        url = self.base_url + suffix
        session = self.local_session
        try:
            if method == "GET":
                response = session.get(url)
            elif method == "POST":
                response = session.post(url, json=json_data)
            elif method == "PUT":
                response = session.put(url, json=json_data)
            elif method == "DELETE":
                response = session.delete(url, json=json_data)
            else:
                raise ValueError(f"Invalid method {method}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during local request to {url}: {e}")
            return None

    def get_region(self):
        response = self.handle_local_request("product-session/v1/external-sessions")
        if response and response.status_code == 200:
            response_json = response.json()
            for key, region_info in response_json.items():
                if key != 'host_app':
                    arguments = region_info.get("launchConfiguration", {}).get("arguments", [])
                    for arg in arguments:
                        if arg.startswith("-ares-deployment="):
                            return arg.split('=')[1]
            raise Exception("Valid region information not found in any non-host_app key.")
        else:
            raise Exception("Failed to get region information.")

    def get_current_version(self):
        response = requests.get("https://valorant-api.com/v1/version")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            raise Exception(f"Failed to get client version: {response.status_code}")

    def get_client_platform(self):
        client_platform_info = {
            "platformType": "PC",
            "platformOS": "Windows",
            "platformOSVersion": "10.0.19042.1.256.64bit",
            "platformChipset": "Unknown"
        }
        return base64.b64encode(json.dumps(client_platform_info).encode('utf-8')).decode('utf-8')

    def get_auth_headers(self):
        auth_info = self.get_auth_info()

        headers = {
            'Authorization': f"Bearer {auth_info[0]}",
            'X-Riot-Entitlements-JWT': auth_info[1],
            'X-Riot-ClientVersion': self.client_version['riotClientVersion'],
            'X-Riot-ClientPlatform': self.client_platform,
            'User-Agent': "ShooterGame/13 Windows/10.0.19043.1.256.64bit"
        }
        return headers

    def get_auth_info(self):
        r = self.local_session.get(f'{self.base_url}entitlements/v1/token')
        if r.status_code == 200:
            response_json = r.json()
            access_token = response_json['accessToken']
            entitlements_token = response_json['token']
            return [access_token, entitlements_token]
        else:
            raise Exception(f"Failed to get entitlements token: {r.status_code} {r.text}")

    def handle_pvp_request(self, suffix, prefix=None, header=None, method="GET", json_data=None, retries=3):
        if header is None:
            header = self.auth_headers

        if prefix and not prefix.startswith('https://'):
            prefix = f"https://{prefix}"

        url = f'{prefix}/{suffix}' if prefix else f'https://{self.pvp_base_url}/{suffix}'

        session = self.session

        for attempt in range(retries):
            try:
                # Handle different request methods
                if method == "GET":
                    response = session.get(url, headers=header)
                elif method == "POST":
                    response = session.post(url, headers=header, json=json_data)
                elif method == "PUT":
                    response = session.put(url, headers=header, json=json_data)
                elif method == "DELETE":
                    response = session.delete(url, headers=header, json=json_data)
                else:
                    raise ValueError(f"Invalid method {method}")

                # Check for errors and return the response or raise exceptions as needed
                if response.status_code == 200:
                    return response
                else:
                    print(f"Request to {url} failed with status code {response.status_code}: {response.text}")
                    return response  # Return the Response object even on failure

            except requests.exceptions.ConnectionError as e:
                print(f"Connection error on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                else:
                    raise

    def get_current_player(self):
        return Request("https://auth.riotgames.com/userinfo", self.base_pvp_header, session=self.session).get_json()

    def get_current_player_puuid(self):
        return self.get_current_player()["sub"]

    @classmethod
    def init_from_lockFile(cls):
        lockFile = cls.parse_lockfile()
        return ValClient("127.0.0.1", lockFile["port"], "riot", lockFile["password"])

    @classmethod
    def parse_lockfile(cls):
        path_ = path.expandvars(r'%LOCALAPPDATA%\\VALORANT\\Saved\\Lockfile')
        if not os.path.exists(path_):
            path_ = path.expandvars(r'%LOCALAPPDATA%\\Riot Games\\Riot Client\\Config\\lockfile')
            if not os.path.exists(path_):
                raise FileNotFoundError(f"Lockfile not found at {path_}. Is Valorant running?")

        with open(path_, "r") as lockFile:
            lockFileContent = lockFile.read()

        riot_client_params = lockFileContent.split(":")
        lock_data = {
            "raw": lockFileContent,
            "name": riot_client_params[0],
            "pid": riot_client_params[1],
            "port": riot_client_params[2],
            "password": riot_client_params[3],
            "protocol": riot_client_params[4]
        }
        return lock_data

    """
    VALORANT SERVERS
    """

    def get_valorant_server_ping(self, region):
        servers_dict = {
            "EU-WEST": "dynamodb.eu-west-3.amazonaws.com",
            "EU-CENTRAL": "dynamodb.eu-central-1.amazonaws.com",
            "EU-NORTH": "dynamodb.eu-north-1.amazonaws.com",
            "NA-WEST": "dynamodb.us-west-1.amazonaws.com",
            "NA-NORTH-WEST": "dynamodb.us-west-2.amazonaws.com",
            "NA-CENTRAL": "dynamodb.us-east-2.amazonaws.com",
            "ASIA-NORTH": "dynamodb.ap-northeast-2.amazonaws.com",
            "ASIA-WEST": "dynamodb.ap-northeast-1.amazonaws.com"
        }
        ping_result = ping(target=servers_dict[region], count=10, timeout=2)
        return {
            'host': servers_dict[region],
            'avg_latency': ping_result.rtt_avg_ms,
            'min_latency': ping_result.rtt_min_ms,
            'max_latency': ping_result.rtt_max_ms,
            'packet_loss': ping_result.packet_loss
        }





    """

    PLAYER ACCOUNT

    """


    def get_current_player(self):
        return Request("https://auth.riotgames.com/userinfo", self.base_pvp_header).get_json()

    def get_current_player_puuid(self):
        return self.get_current_player()["sub"]
