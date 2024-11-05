class PartyEndpoints:
    def __init__(self, api):
        self.api = api

    def get_current_party_id(self):
        party_data = self.get_current_party()
        if party_data:
            return party_data.get("CurrentPartyID")
        else:
            print("No current party data available.")
            return None

    def get_current_party_from_id(self, partyID):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}", prefix=prefix, header=header)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get party from ID: {response.status_code if response else 'No response'}")
            return None

    def get_current_party(self):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/players/{self.api.get_current_player_puuid()}", prefix=prefix, header=header)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get current party: {response.status_code if response else 'No response'}")
            return None

    def kick_player_from_party(self, puuid):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/players/{puuid}", prefix=prefix, header=header, method="DELETE")
        if response and response.status_code == 200:
            print("Player kicked from party successfully.")
            return True
        else:
            print(f"Failed to kick player from party: {response.status_code if response else 'No response'}")
            return False

    def set_player_ready(self, state=False):
        partyID = self.get_current_party_id()
        puuid = self.api.get_current_player_puuid()
        if not partyID:
            print("Cannot set player ready: No party ID found.")
            return False
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        data = {"ready": state}
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/members/{puuid}/setReady",
                                               prefix=prefix, header=header, method="POST", json_data=data)
        if response and response.status_code == 200:
            print("Player ready state updated successfully.")
            return True
        else:
            print(f"Failed to set player ready state: {response.status_code if response else 'No response'}")
            return False

    def party_refresh_competitive_tier(self):
        partyID = self.get_current_party_id()
        puuid = self.api.get_current_player_puuid()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/members/{puuid}/refreshCompetitiveTier",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Competitive tier refreshed successfully.")
            return True
        else:
            print(f"Failed to refresh competitive tier: {response.status_code if response else 'No response'}")
            return False

    def refresh_player_id(self):
        partyID = self.get_current_party_id()
        puuid = self.api.get_current_player_puuid()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/members/{puuid}/refreshPlayerIdentity",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Player identity refreshed successfully.")
            return True
        else:
            print(f"Failed to refresh player identity: {response.status_code if response else 'No response'}")
            return False

    def refresh_party_ping(self):
        partyID = self.get_current_party_id()
        puuid = self.api.get_current_player_puuid()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/members/{puuid}/refreshPings",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Ping refreshed successfully.")
            return True
        else:
            print(f"Failed to refresh ping: {response.status_code if response else 'No response'}")
            return False

    def join_queue(self):
        partyID = self.get_current_party_id()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/matchmaking/join",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Joined queue successfully.")
            return True
        else:
            print(f"Failed to join queue: {response.status_code if response else 'No response'}")
            return False

    def leave_queue(self):
        partyID = self.get_current_party_id()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/matchmaking/leave",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Left queue successfully.")
            return True
        else:
            print(f"Failed to leave queue: {response.status_code if response else 'No response'}")
            return False

    def set_party_accessibility(self, accessibility=True):
        partyID = self.get_current_party_id()
        accessibility_dict = {True: "OPEN", False: "CLOSED"}
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        data = {"accessibility": accessibility_dict[accessibility]}
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/accessibility",
                                               prefix=prefix, header=header, method="POST", json_data=data)
        if response and response.status_code == 200:
            print("Party accessibility updated successfully.")
            return True
        else:
            print(f"Failed to update party accessibility: {response.status_code if response else 'No response'}")
            return False

    def party_invite(self, displayName):
        displayName = displayName.split("#")
        gameName = displayName[0]
        tagLine = displayName[1]
        partyID = self.get_current_party_id()
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        header["X-Riot-ClientVersion"] = self.api.client_version['riotClientVersion']
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/invites/name/{gameName}/tag/{tagLine}",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Party invite sent successfully.")
            return True
        else:
            print(f"Failed to send party invite: {response.status_code if response else 'No response'}")
            return False

    def party_request_join(self, partyID):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/request",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Party join request sent successfully.")
            return True
        else:
            print(f"Failed to send party join request: {response.status_code if response else 'No response'}")
            return False

    def decline_party_request(self, partyID, requestID):
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = self.api.get_auth_info()[1]
        prefix = self.api.get_glz_url()
        response = self.api.handle_pvp_request(f"parties/v1/parties/{partyID}/request/{requestID}/decline",
                                               prefix=prefix, header=header, method="POST")
        if response and response.status_code == 200:
            print("Party request declined successfully.")
            return True
        else:
            print(f"Failed to decline party request: {response.status_code if response else 'No response'}")
            return False
