class LocalEndpoints:
    def __init__(self, api):
        self.api = api

    def get_friends(self):
        """
        Fetch the list of friends.

        Returns:
            dict: JSON response containing the list of friends.
        """
        response = self.api.handle_local_request("chat/v4/friends")
        return response.json() if response and response.status_code == 200 else None

    def get_friend_requests(self):
        """
        Fetch the list of pending friend requests.

        Returns:
            dict: JSON response containing the list of friend requests.
        """
        response = self.api.handle_local_request("chat/v4/friend_requests")
        return response.json() if response and response.status_code == 200 else None

    def add_friend(self, game_name, tag_line):
        """
        Add a friend by their in-game name and tag.

        Args:
            game_name (str): The game name of the friend.
            tag_line (str): The tag line of the friend.

        Returns:
            bool: True if the friend was added successfully, False otherwise.
        """
        data = {'game_name': game_name, 'game_tag': tag_line}
        response = self.api.handle_local_request("chat/v4/friends", method="POST", json_data=data)
        return response.status_code == 200 if response else False

    def remove_friend(self, puuid):
        """
        Remove a friend by their PUUID.

        Args:
            puuid (str): The PUUID of the friend to remove.

        Returns:
            bool: True if the friend was removed successfully, False otherwise.
        """
        data = {"puuid": puuid}
        response = self.api.handle_local_request("chat/v4/friends", method="DELETE", json_data=data)
        return response.status_code == 200 if response else False

    def get_messages(self):
        """
        Fetch the list of messages in the chat.

        Returns:
            dict: JSON response containing the list of messages.
        """
        response = self.api.handle_local_request("chat/v5/messages")
        return response.json() if response and response.status_code == 200 else None

    def send_message(self, message, cid):
        """
        Send a message to a specific chat channel.

        Args:
            message (str): The message content.
            cid (str): The chat channel ID.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        data = {"message": message, "cid": cid}
        response = self.api.handle_local_request("chat/v5/messages", method="POST", json_data=data)
        return response.status_code == 200 if response else False

    def get_auth_info(self):
        """
        Fetch the authentication token and entitlements token.

        Returns:
            list: [access_token, entitlements_token] if successful, None otherwise.
        """
        response = self.api.handle_local_request("entitlements/v1/token")
        if response and response.status_code == 200:
            response_json = response.json()
            return [response_json["accessToken"], response_json["token"]]
        return None

    def get_player_settings(self):
        """
        Fetch the player's settings.

        Returns:
            dict: JSON response containing the player's settings.
        """
        response = self.api.handle_local_request("player-preferences/v1/data-json/Ares.PlayerSettings")
        return response.json() if response and response.status_code == 200 else None

    def get_presence(self):
        """
        Fetch the presence data for the player.

        Returns:
            list: JSON response containing the player's presence data.
        """
        response = self.api.handle_local_request("chat/v4/presences")
        return response.json().get("presences", []) if response and response.status_code == 200 else None

    def get_session(self):
        """
        Fetch the current session information.

        Returns:
            dict: JSON response containing the session information.
        """
        response = self.api.handle_local_request("session/v1/sessions")
        return response.json() if response and response.status_code == 200 else None

    def get_region(self):
        """
        Fetch the player's region.

        Returns:
            str: The player's region if successful, None otherwise.
        """
        response = self.api.handle_local_request("product-session/v1/external-sessions")
        if response and response.status_code == 200:
            response_json = response.json()
            for key, region_info in response_json.items():
                if key != 'host_app':
                    arguments = region_info.get("launchConfiguration", {}).get("arguments", [])
                    for arg in arguments:
                        if arg.startswith("-ares-deployment="):
                            return arg.split('=')[1]
        return None

    def get_voice_settings(self):
        """
        Fetch the player's voice settings.

        Returns:
            dict: JSON response containing the voice settings.
        """
        response = self.api.handle_local_request("voice-chat/v1/settings")
        return response.json() if response and response.status_code == 200 else None

    def update_voice_settings(self, settings):
        """
        Update the player's voice settings.

        Args:
            settings (dict): The new voice settings.

        Returns:
            bool: True if the settings were updated successfully, False otherwise.
        """
        response = self.api.handle_local_request("voice-chat/v1/settings", method="PUT", json_data=settings)
        return response.status_code == 200 if response else False

    def get_voice_token(self):
        """
        Fetch the voice token for the player.

        Returns:
            dict: JSON response containing the voice token.
        """
        response = self.api.handle_local_request("voice-chat/v1/token")
        return response.json() if response and response.status_code == 200 else None

    def get_voice_state(self):
        """
        Fetch the player's voice state.

        Returns:
            dict: JSON response containing the voice state.
        """
        response = self.api.handle_local_request("voice-chat/v1/state")
        return response.json() if response and response.status_code == 200 else None

    def get_voice_participants(self):
        """
        Fetch the list of participants in the voice chat.

        Returns:
            dict: JSON response containing the list of participants.
        """
        response = self.api.handle_local_request("voice-chat/v1/participants")
        return response.json() if response and response.status_code == 200 else None

    def get_voice_devices(self):
        """
        Fetch the list of available voice devices.

        Returns:
            dict: JSON response containing the list of voice devices.
        """
        response = self.api.handle_local_request("voice-chat/v1/devices")
        return response.json() if response and response.status_code == 200 else None

    def get_voice_connections(self):
        """
        Fetch the list of active voice connections.

        Returns:
            dict: JSON response containing the list of voice connections.
        """
        response = self.api.handle_local_request("voice-chat/v1/connections")
        return response.json() if response and response.status_code == 200 else None
