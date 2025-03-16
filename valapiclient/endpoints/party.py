class PartyEndpoints:
    def __init__(self, api):
        self.api = api

    def build_glz_url(self, endpoint):
        return f"https://glz-{self.api.region}-1.{self.api.region}.a.pvp.net/{endpoint}"

    def get_current_party_id(self):
        """
        Fetch the current party ID for the logged-in player.

        Returns:
            str: The current party ID if successful, None otherwise.
        """
        response = self.api.handle_pvp_request(
            f"parties/v1/players/{self.api.get_current_player_puuid()}",
            prefix=self.build_glz_url("")
        )
        return response.json().get("CurrentPartyID") if response and response.status_code == 200 else None

    def get_current_party(self):
        """
        Fetch the current party information.

        Returns:
            dict: JSON response containing the current party information.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return None

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}",
            prefix=self.build_glz_url("")
        )
        return response.json() if response and response.status_code == 200 else None

    def kick_player_from_party(self, puuid):
        """
        Kick a player from the current party.

        Args:
            puuid (str): The PUUID of the player to kick.

        Returns:
            bool: True if the player was kicked successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/members/{puuid}",
            prefix=self.build_glz_url(""),
            method="DELETE"
        )
        return response.status_code == 200 if response else False

    def set_player_ready(self, state=True):
        """
        Set the player's ready state in the party.

        Args:
            state (bool): True to set ready, False to set not ready.

        Returns:
            bool: True if the ready state was updated successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        data = {"ready": state}
        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/members/{self.api.get_current_player_puuid()}/setReady",
            prefix=self.build_glz_url(""),
            method="POST",
            json_data=data
        )
        return response.status_code == 200 if response else False

    def refresh_competitive_tier(self):
        """
        Refresh the competitive tier for the player in the party.

        Returns:
            bool: True if the competitive tier was refreshed successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/members/{self.api.get_current_player_puuid()}/refreshCompetitiveTier",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def refresh_player_identity(self):
        """
        Refresh the player's identity in the party.

        Returns:
            bool: True if the player's identity was refreshed successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/members/{self.api.get_current_player_puuid()}/refreshPlayerIdentity",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def refresh_party_ping(self):
        """
        Refresh the party's ping.

        Returns:
            bool: True if the party's ping was refreshed successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/members/{self.api.get_current_player_puuid()}/refreshPings",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def join_queue(self):
        """
        Join the matchmaking queue.

        Returns:
            bool: True if the player joined the queue successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/matchmaking/join",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def leave_queue(self):
        """
        Leave the matchmaking queue.

        Returns:
            bool: True if the player left the queue successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/matchmaking/leave",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def set_party_accessibility(self, accessibility=True):
        """
        Set the party's accessibility (open or closed).

        Args:
            accessibility (bool): True to set the party as open, False to set it as closed.

        Returns:
            bool: True if the party's accessibility was updated successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        accessibility_dict = {True: "OPEN", False: "CLOSED"}
        data = {"accessibility": accessibility_dict[accessibility]}
        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/accessibility",
            prefix=self.build_glz_url(""),
            method="POST",
            json_data=data
        )
        return response.status_code == 200 if response else False

    def invite_player(self, game_name, tag_line):
        """
        Invite a player to the party by their in-game name and tag.

        Args:
            game_name (str): The game name of the player to invite.
            tag_line (str): The tag line of the player to invite.

        Returns:
            bool: True if the invite was sent successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/invites/name/{game_name}/tag/{tag_line}",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def request_to_join_party(self, party_id):
        """
        Request to join a party by its ID.

        Args:
            party_id (str): The ID of the party to join.

        Returns:
            bool: True if the request was sent successfully, False otherwise.
        """
        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/request",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False

    def decline_party_request(self, request_id):
        """
        Decline a party join request.

        Args:
            request_id (str): The ID of the request to decline.

        Returns:
            bool: True if the request was declined successfully, False otherwise.
        """
        party_id = self.get_current_party_id()
        if not party_id:
            return False

        response = self.api.handle_pvp_request(
            f"parties/v1/parties/{party_id}/request/{request_id}/decline",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False
