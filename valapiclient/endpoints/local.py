class LocalEndpoints:
    def __init__(self, api):
        self.api = api

    def get_friends(self):
        response = self.api.handle_local_request("chat/v4/friends")
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get friends: {response.status_code if response else 'No response'}")
            return None

    def get_friend_requests(self):
        response = self.api.handle_local_request("chat/v4/friend_requests")
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get friend requests: {response.status_code if response else 'No response'}")
            return None

    def add_friend(self, gameName, tagLine):
        data = {'game_name': gameName, 'game_tag': tagLine}
        response = self.api.handle_local_request("chat/v4/friends", method="POST", json_data=data)
        if response and response.status_code == 200:
            return True
        else:
            print(f"Failed to add friend: {response.status_code if response else 'No response'} - {response.text if response else ''}")
            return False

    def remove_friend(self, puuid):
        data = {"puuid": puuid}
        response = self.api.handle_local_request("chat/v4/friends", method="DELETE", json_data=data)
        if response and response.status_code == 200:
            return True
        else:
            print(f"Failed to remove friend: {response.status_code if response else 'No response'}")
            return False

    def get_messages(self):
        response = self.api.handle_local_request("chat/v5/messages")
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get messages: {response.status_code if response else 'No response'}")
            return None

    def send_message(self, message, cid):
        data = {"message": message, "cid": cid}
        response = self.api.handle_local_request("chat/v5/messages", method="POST", json_data=data)
        if response and response.status_code == 200:
            return True
        else:
            print(f"Failed to send message: {response.status_code if response else 'No response'}")
            return False

    def get_auth_info(self):
        response = self.api.handle_local_request("entitlements/v1/token")
        if response and response.status_code == 200:
            response_json = response.json()
            return [response_json["accessToken"], response_json["token"]]
        else:
            print(f"Failed to get auth info: {response.status_code if response else 'No response'}")
            return None

    def get_player_settings(self):
        response = self.api.handle_local_request("player-preferences/v1/data-json/Ares.PlayerSettings")
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get player settings: {response.status_code if response else 'No response'}")
            return None

    def get_presence(self):
        response = self.api.handle_local_request("chat/v4/presences")
        if response and response.status_code == 200:
            return response.json().get("presences", [])
        else:
            print(f"Failed to get presence data: {response.status_code if response else 'No response'}")
            return None