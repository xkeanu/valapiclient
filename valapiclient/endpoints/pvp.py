import requests
from typing import Optional, Dict, List, Union

class PvPEndpoints:
    def __init__(self, api):
        self.api = api

    def _get_auth_header(self) -> Optional[Dict[str, str]]:
        """Helper function to fetch authentication headers."""
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header = self.api.base_pvp_header.copy()
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        return header

    def _validate_puuid(self, puuid: str) -> bool:
        """Helper function to validate a PUUID."""
        if not puuid or not isinstance(puuid, str):
            print("Invalid PUUID.")
            return False
        return True

    def get_content(self) -> Optional[Dict]:
        """Fetches the current content (e.g., maps, agents, etc.) from the Valorant API."""
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request("content-service/v3/content", prefix=prefix, header=header)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return None

    def get_account_xp(self, puuid: str) -> Optional[Dict]:
        """Fetches the account XP for a given player (PUUID)."""
        if not self._validate_puuid(puuid):
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request(f"account-xp/v1/players/{puuid}", prefix=prefix, header=header)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account XP: {e}")
            return None

    def get_player_mmr(self, puuid: str) -> Optional[Dict]:
        """Fetches the matchmaking rating (MMR) for a given player (PUUID)."""
        if not self._validate_puuid(puuid):
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_pd_url()
            response = self.api.handle_pvp_request(f"mmr/v1/players/{puuid}", prefix=prefix, header=header)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player MMR: {e}")
            return None

    def get_match_history(self, puuid: str, start_index: int = 0, end_index: int = 20) -> Optional[Dict]:
        """Fetches the match history for a given player (PUUID)."""
        if not self._validate_puuid(puuid):
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request(
                f"match-history/v1/history/{puuid}?startIndex={start_index}&endIndex={end_index}",
                prefix=prefix,
                header=header
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching match history: {e}")
            return None

    def get_current_game(self, puuid: str) -> Optional[Dict]:
        """Fetches the current game details for a given player (PUUID)."""
        if not self._validate_puuid(puuid):
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request(f"current-game/v1/players/{puuid}", prefix=prefix, header=header)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current game: {e}")
            return None

    def get_leaderboard(self, season_id: str, start_index: int = 0, end_index: int = 20) -> Optional[Dict]:
        """Fetches the leaderboard for a given season."""
        if not season_id or not isinstance(season_id, str):
            print("Invalid season ID.")
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request(
                f"leaderboards/v2/{season_id}?startIndex={start_index}&endIndex={end_index}",
                prefix=prefix,
                header=header
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching leaderboard: {e}")
            return None

    def get_competitive_updates(self, puuid: str, start_index: int = 0, end_index: int = 20) -> Optional[Dict]:
        """Fetches competitive updates for a given player (PUUID)."""
        if not self._validate_puuid(puuid):
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            prefix = self.api.get_shared_url()
            response = self.api.handle_pvp_request(
                f"competitive-updates/v1/players/{puuid}?startIndex={start_index}&endIndex={end_index}",
                prefix=prefix,
                header=header
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching competitive updates: {e}")
            return None

    def get_player_name(self, puuids: Union[str, List[str]]) -> Optional[List[Dict]]:
        """
        Fetches player names and taglines by their PUUIDs.
        
        Args:
            puuids: Single UUID string or list of player UUIDs to look up
            
        Returns:
            List of dictionaries containing player name information:
            [
                {
                    "DisplayName": str,
                    "Subject": str,
                    "GameName": str,
                    "TagLine": str
                },
                ...
            ]
        """
        # Convert single UUID to list
        if isinstance(puuids, str):
            puuids = [puuids]
            
        if not puuids or not isinstance(puuids, list) or not all(isinstance(p, str) for p in puuids):
            print("Invalid PUUID(s).")
            return None
            
        try:
            header = self._get_auth_header()
            if not header:
                return None
                
            prefix = self.api.get_pd_url()
            response = self.api.handle_pvp_request(
                "name-service/v2/players",
                method="PUT",
                prefix=prefix,
                header=header,
                json_data=puuids
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player names: {e}")
            return None

    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """
        Fetches the details of a specific match by its ID.

        Args:
            match_id: The ID of the match to fetch details for.

        Returns:
            A dictionary containing the match details, or None if an error occurs.
        """
        if not match_id or not isinstance(match_id, str):
            print("Invalid Match ID.")
            return None
        try:
            header = self._get_auth_header()
            if not header:
                return None
            # The get_pd_url() method should construct the base URL including the shard
            prefix = self.api.get_pd_url() 
            response = self.api.handle_pvp_request(
                f"match-details/v1/matches/{match_id}",
                prefix=prefix,
                header=header
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching match details for match ID {match_id}: {e}")
            return None
