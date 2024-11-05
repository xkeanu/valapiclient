class CoreGameEndpoints:
    def __init__(self, api):
        self.api = api

    def get_current_match_id(self):
        puuid = self.api.get_current_player_puuid()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]

        # Use the full GLZ URL
        prefix = self.api.get_glz_url()

        response = self.api.handle_pvp_request(
            f"core-game/v1/players/{puuid}",
            prefix=prefix,
            header=header
        )

        if response is not None and response.status_code == 200:
            data = response.json()
            return data.get("MatchID")
        else:
            print(f"Failed to get current match ID: {response.status_code} - {response.text}")
            return None

    def get_current_match_info(self, matchID):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]

        # Use the full GLZ URL
        prefix = self.api.get_glz_url()

        response = self.api.handle_pvp_request(
            f"core-game/v1/matches/{matchID}",
            prefix=prefix,
            header=header
        )

        if response is not None and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get current match info: {response.status_code} - {response.text}")
            return None

    def get_current_match_loadout(self, matchID):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]

        # Use the full GLZ URL
        prefix = self.api.get_glz_url()

        response = self.api.handle_pvp_request(
            f"core-game/v1/matches/{matchID}/loadouts",
            prefix=prefix,
            header=header
        )

        if response is not None and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get current match loadout: {response.status_code} - {response.text}")
            return None

    def leave_current_match(self):
        puuid = self.api.get_current_player_puuid()
        matchID = self.get_current_match_id()

        if matchID is None:
            print("No current match ID found.")
            return False

        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        print(f"Attempting to leave match: Player UUID: {puuid}, Match ID: {matchID}")

        # Use the full GLZ URL
        prefix = self.api.get_glz_url()

        response = self.api.handle_pvp_request(
            f"core-game/v1/players/{puuid}/disassociate/{matchID}",
            prefix=prefix,
            header=header,
            method="POST"
        )

        if response is not None:
            if response.status_code == 200:
                print("Successfully left the match.")
                return True
            else:
                print(f"Failed to leave the match: {response.status_code} - {response.text}")
                return False
        else:
            print("Failed to leave the match: No response.")
            return False
