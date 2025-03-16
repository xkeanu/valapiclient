class PreGameEndpoints:
    def __init__(self, api):
        self.api = api

    def build_glz_url(self, endpoint):
        return f"https://glz-{self.api.region}-1.{self.api.region}.a.pvp.net/{endpoint}"

    def get_current_pregame(self, puuid):
        """
        Fetch the current pregame lobby for the specified player.

        Args:
            puuid (str): Player's unique identifier.

        Returns:
            dict: JSON response containing pregame lobby data.
        """
        try:
            response = self.api.handle_pvp_request(
                f"pregame/v1/players/{puuid}",
                prefix=self.build_glz_url("")
            )
            if response and response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch pregame data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_current_pregame_id(self):
        """Fetch the current pregame match ID for the logged-in player."""
        pregame_data = self.get_current_pregame(self.api.get_current_player_puuid())
        return pregame_data.get("MatchID") if pregame_data else None

    def select_pregame_agent(self, agent_id):
        """
        Select (hover) an agent in the pregame lobby.

        Args:
            agent_id (str): The ID of the agent to select.

        Returns:
            dict: JSON response from the API.
        """
        match_id = self.get_current_pregame_id()
        if not match_id:
            print("No active pregame match found.")
            return None

        return self.api.handle_pvp_request(
            f"pregame/v1/matches/{match_id}/select/{agent_id}",
            prefix=self.build_glz_url(""),
            method="POST"
        ).json()

    def lock_pregame_agent(self, agent_id):
        """
        Lock in an agent in the pregame lobby.

        Args:
            agent_id (str): The ID of the agent to lock.

        Returns:
            dict: JSON response from the API.
        """
        match_id = self.get_current_pregame_id()
        if not match_id:
            print("No active pregame match found.")
            return None

        return self.api.handle_pvp_request(
            f"pregame/v1/matches/{match_id}/lock/{agent_id}",
            prefix=self.build_glz_url(""),
            method="POST"
        ).json()

    def dodge_pregame_match(self):
        """Quit the current pregame match."""
        match_id = self.get_current_pregame_id()
        if not match_id:
            print("No active pregame match found.")
            return None

        return self.api.handle_pvp_request(
            f"pregame/v1/matches/{match_id}/quit",
            prefix=self.build_glz_url(""),
            method="POST"
        ).json()
