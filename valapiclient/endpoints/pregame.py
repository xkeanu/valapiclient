class PreGameEndpoints:
    def __init__(self, api):
        self.api = api

    def get_current_pregame(self, puuid):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = f"glz-{self.api.region}-1.{self.api.region}.a.pvp.net"
        response = self.api.handle_pvp_request(
            f"pregame/v1/players/{puuid}",
            prefix=prefix,
            header=header
        )
        if response is not None:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get pregame data: {response.status_code} - {response.text}")
                return None
        else:
            print("Failed to get pregame data: No response")
            return None

    def get_current_pregame_id(self):
        pregame_data = self.get_current_pregame(self.api.get_current_player_puuid())
        if pregame_data:
            return pregame_data.get("MatchID", None)
        else:
            print("Pregame data is None.")
            return None

    def select_pregame_agent(self, agentID):
        matchID = self.get_current_pregame_id()
        if matchID is None:
            print("No current pregame match found.")
            return None

        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientPlatform"] = self.api.client_platform
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']

        url = f"pregame/v1/matches/{matchID}/select/{agentID}"
        prefix = f"glz-{self.api.region}-1.{self.api.region}.a.pvp.net"
        response = self.api.handle_pvp_request(url, prefix=prefix, header=header, method="POST")

        if response is not None:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                return None
        else:
            print("Error: Request object is None.")
            return None

    def lock_pregame_agent(self, agentID):
        matchID = self.get_current_pregame_id()
        if matchID is None:
            print("No current pregame match found.")
            return None

        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = f"glz-{self.api.region}-1.{self.api.region}.a.pvp.net"
        response = self.api.handle_pvp_request(
            f"pregame/v1/matches/{matchID}/lock/{agentID}",
            prefix=prefix,
            header=header,
            method="POST"
        )
        if response is not None:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                return None
        else:
            print("Error: Request object is None.")
            return None

    def dodge_pregame_match(self):
        matchID = self.get_current_pregame_id()
        if matchID is None:
            print("No current pregame match found.")
            return None

        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = f"glz-{self.api.region}-1.{self.api.region}.a.pvp.net"
        response = self.api.handle_pvp_request(
            f"pregame/v1/matches/{matchID}/quit",
            prefix=prefix,
            header=header,
            method="POST"
        )
        if response is not None:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                return None
        else:
            print("Error: Request object is None.")
            return None
