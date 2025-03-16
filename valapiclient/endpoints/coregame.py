class CoreGameEndpoints:
    def __init__(self, api):
        self.api = api

    def build_glz_url(self, endpoint):
        return f"https://glz-{self.api.region}-1.{self.api.region}.a.pvp.net/{endpoint}"

    def get_current_match_id(self):
        """Fetch the current match ID for the logged-in player."""
        puuid = self.api.get_current_player_puuid()
        response = self.api.handle_pvp_request(
            f"core-game/v1/players/{puuid}",
            prefix=self.build_glz_url("")
        )
        return response.json().get("MatchID") if response and response.status_code == 200 else None

    def get_current_match_info(self, match_id):
        """Fetch detailed information for a specific match.

        Args:
            match_id (str): The ID of the match.

        Returns:
            dict: JSON response containing match details.
        """
        if not match_id:
            print("Invalid match ID.")
            return None

        response = self.api.handle_pvp_request(
            f"core-game/v1/matches/{match_id}",
            prefix=self.build_glz_url("")
        )
        return response.json() if response and response.status_code == 200 else None

    def get_current_match_loadout(self, match_id):
        """Fetch loadout information for a specific match.

        Args:
            match_id (str): The ID of the match.

        Returns:
            dict: JSON response containing loadout details.
        """
        if not match_id:
            print("Invalid match ID.")
            return None

        response = self.api.handle_pvp_request(
            f"core-game/v1/matches/{match_id}/loadouts",
            prefix=self.build_glz_url("")
        )
        return response.json() if response and response.status_code == 200 else None

    def leave_current_match(self):
        """Leave the current match."""
        puuid = self.api.get_current_player_puuid()
        match_id = self.get_current_match_id()
        if not match_id:
            print("No active match found.")
            return False

        response = self.api.handle_pvp_request(
            f"core-game/v1/players/{puuid}/disassociate/{match_id}",
            prefix=self.build_glz_url(""),
            method="POST"
        )
        return response.status_code == 200 if response else False
