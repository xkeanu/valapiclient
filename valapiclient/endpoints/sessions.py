class SessionsEndpoints:
    def __init__(self, api):
        self.api = api

    def get_session(self, puuid):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        header["X-Riot-ClientPlatform"] = self.api.client_platform
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"session/v1/sessions/{puuid}", prefix=prefix, header=header)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get session: {response.status_code if response else 'No response'}")
            return None
