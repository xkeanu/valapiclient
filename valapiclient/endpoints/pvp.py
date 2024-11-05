class PvPEndpoints:
    def __init__(self, api):
        self.api = api

    def get_content(self):
        header = self.api.base_pvp_header.copy()
        header.update({
            "X-Riot-ClientPlatform": self.api.client_platform,
            "X-Riot-ClientVersion": self.api.client_version['riotClientVersion']
        })
        prefix = self.api.get_shared_url()
        response = self.api.handle_pvp_request("content-service/v3/content", prefix=prefix, header=header)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get content: {response.status_code if response else 'No response'}")
            return None

    def get_account_xp(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"account-xp/v1/players/{puuid}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get account XP: {response.status_code if response else 'No response'}")
            return None

    def get_player_loadout(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"personalization/v2/players/{puuid}/playerloadout", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get player loadout: {response.status_code if response else 'No response'}")
            return None

    def update_player_loadout(self, puuid: str, new_loadout: dict) -> bool:
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return False
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"personalization/v2/players/{puuid}/playerloadout",
                                               header=header, method="PUT", json_data=new_loadout, prefix=prefix)
        if response and response.status_code == 200:
            print("Player loadout updated successfully.")
            return True
        else:
            print(f"Failed to update player loadout: {response.status_code if response else 'No response'}")
            return False

    def get_player_mmr(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        header.update({
            "X-Riot-ClientPlatform": self.api.client_platform,
            "X-Riot-ClientVersion": self.api.client_version['riotClientVersion'],
            "X-Riot-Entitlements-JWT": self.api.get_auth_info()[1]
        })
        response = self.api.handle_pvp_request(f"mmr/v1/players/{puuid}", header=header)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get player MMR: {response.status_code if response else 'No response'}")
            return None

    def get_match_history(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"match-history/v1/history/{puuid}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get match history: {response.status_code if response else 'No response'}")
            return None

    def get_match_details(self, matchID: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"match-details/v1/matches/{matchID}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get match details: {response.status_code if response else 'No response'}")
            return None

    def get_player_restrictions(self):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request("restrictions/v3/penalties", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get player restrictions: {response.status_code if response else 'No response'}")
            return None

    def get_player_name(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        header["Authorization"] = f"Bearer {auth_info[0]}"
        prefix = self.api.get_pd_url()
        body = [puuid]

        response = self.api.handle_pvp_request("name-service/v2/players", prefix=prefix, header=header, method="PUT", json_data=body)
        if response and response.status_code == 200:
            player_info = response.json()[0]
            return {
                "DisplayName": player_info.get("DisplayName"),
                "GameName": player_info.get("GameName"),
                "TagLine": player_info.get("TagLine")
            }
        else:
            print(f"Failed to retrieve player name: {response.status_code if response else 'No response'}")
            return None
