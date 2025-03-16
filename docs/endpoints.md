# Valorant API Endpoints Documentation

This document provides detailed information about the available endpoint classes in the ValorantAPIClient library.

## Party Endpoints

The Party endpoints (`api.party`) allow you to manage party-related operations.

### Methods

#### `get_current_party_id()`
- Returns the current party ID for the logged-in player
- Returns: `str` (party ID) or `None` if unsuccessful

#### `get_current_party()`
- Fetches complete information about the current party
- Returns: `dict` containing party information or `None` if unsuccessful

#### `kick_player_from_party(puuid)`
- Kicks a player from the current party
- Args:
  - `puuid` (str): Player UUID to kick
- Returns: `bool` indicating success/failure

#### `set_player_ready(state=True)`
- Sets the player's ready status in party
- Args:
  - `state` (bool): True for ready, False for not ready
- Returns: `bool` indicating success/failure

#### `join_queue()`
- Joins the matchmaking queue
- Returns: `bool` indicating success/failure

#### `leave_queue()`
- Leaves the matchmaking queue
- Returns: `bool` indicating success/failure

#### `set_party_accessibility(accessibility=True)`
- Sets party as open or closed
- Args:
  - `accessibility` (bool): True for open, False for closed
- Returns: `bool` indicating success/failure

#### `invite_player(game_name, tag_line)`
- Invites a player to the party
- Args:
  - `game_name` (str): Player's game name
  - `tag_line` (str): Player's tag line
- Returns: `bool` indicating success/failure

## Core Game Endpoints

The Core Game endpoints (`api.coregame`) handle in-game operations.

### Methods

#### `get_match()`
- Gets information about the current match
- Returns: `dict` containing match information or `None`

#### `get_loadout()`
- Gets the player's current loadout
- Returns: `dict` containing loadout information or `None`

#### `get_match_state()`
- Gets the current state of the match
- Returns: `str` representing match state or `None`

## Store Endpoints

The Store endpoints (`api.store`) handle store-related operations.

### Methods

#### `get_offers()`
- Gets current store offers
- Returns: `dict` containing store offers or `None`

#### `get_wallet()`
- Gets player wallet information
- Returns: `dict` containing wallet details or `None`

## Session Endpoints

The Session endpoints (`api.sessions`) handle session management.

### Methods

#### `get_session()`
- Gets current session information
- Returns: `dict` containing session details or `None`

#### `end_session()`
- Ends the current session
- Returns: `bool` indicating success/failure

## Client Utility Methods

### Region and Shards

The Valorant API uses different shards for different regions:

| Shard | Regions |
|-------|---------|
| na | NA, LATAM, BR |
| pbe | PBE |
| eu | EU |
| ap | AP |
| kr | KR |

The client automatically detects the appropriate region/shard from the game's log files or defaults to 'eu' if unavailable.

### Request Headers

All API requests require specific headers:
- `X-Riot-ClientPlatform`: Base64 encoded client platform info
- `X-Riot-ClientVersion`: Current client version
- `X-Riot-Entitlements-JWT`: Entitlement token
- `Authorization`: Bearer token

These are automatically handled by the client implementation.

## Client Utility Methods

The base client (`ValClient`) provides several utility methods:

### Authentication & Setup

#### `init_from_lockFile()`
- Static method to initialize client from Valorant's lockfile
- Returns: Initialized `ValClient` instance

#### `get_auth_info()`
- Retrieves authentication tokens
- Returns: List containing [access_token, entitlements_token]

### Server Information

#### `get_valorant_server_ping(region)`
- Gets ping information for specified server region
- Args:
  - `region` (str): One of EU-WEST, EU-CENTRAL, EU-NORTH, NA-WEST, NA-NORTH-WEST, NA-CENTRAL, ASIA-NORTH, ASIA-WEST
- Returns: `dict` containing:
  - `host`: Server hostname
  - `avg_latency`: Average latency in ms
  - `min_latency`: Minimum latency in ms
  - `max_latency`: Maximum latency in ms
  - `packet_loss`: Packet loss percentage

### Player Information

#### `get_current_player()`
- Gets information about the currently logged-in player
- Returns: `dict` containing player information

#### `get_current_player_puuid()`
- Gets the PUUID of the currently logged-in player
- Returns: `str` containing player UUID

## Player Stats Endpoints

### MMR Information

The client provides access to player MMR (Matchmaking Rating) information through the PvP endpoints. MMR requests are made to the `pd.{region}.a.pvp.net` endpoint:

#### `get_mmr(puuid)`
- Gets detailed MMR information for a player
- Args:
  - `puuid` (str): Player UUID to lookup
- Returns: `dict` containing:
  - Version number
  - Player UUID
  - New player experience status
  - Queue skills
  - Seasonal information
  - Latest competitive update
  - Leaderboard anonymization status
  - Act rank badge visibility

Example response structure:
```python
{
    "Version": number,
    "Subject": str,  # Player UUID
    "NewPlayerExperienceFinished": bool,
    "QueueSkills": {
        "competitive": {
            "TotalGamesNeededForRating": number,
            "TotalGamesNeededForLeaderboard": number,
            "CurrentSeasonGamesNeededForRating": number,
            "SeasonalInfoBySeasonID": {
                "seasonID": {
                    "SeasonID": str,
                    "NumberOfWins": number,
                    "NumberOfGames": number,
                    "Rank": number,
                    "CapstoneWins": number,
                    "LeaderboardRank": number,
                    "CompetitiveTier": number,
                    "RankedRating": number,
                    "WinsByTier": dict,
                    "GamesNeededForRating": number,
                    "TotalWinsNeededForRank": number
                }
            }
        }
    },
    "LatestCompetitiveUpdate": {
        "MatchID": str,
        "MapID": str,
        "SeasonID": str,
        "MatchStartTime": number,
        "TierAfterUpdate": number,
        "TierBeforeUpdate": number,
        "RankedRatingAfterUpdate": number,
        "RankedRatingBeforeUpdate": number,
        "RankedRatingEarned": number,
        "RankedRatingPerformanceBonus": number,
        "CompetitiveMovement": str,
        "AFKPenalty": number
    },
    "IsLeaderboardAnonymized": bool,
    "IsActRankBadgeHidden": bool
}
```

## Error Handling

Most methods return `None` or `False` on failure. The client includes built-in retry logic for network operations. For detailed error information, check the response status codes and messages returned by the API calls.

Common error scenarios:
- 503 Service Unavailable: Server is temporarily unavailable
- 400 Bad Request: Invalid parameters or headers
- 401 Unauthorized: Invalid authentication tokens
- 404 Not Found: Resource not found

## Best Practices

1. Always check return values for `None` or `False` to handle errors gracefully
2. Use appropriate error handling when making API calls
3. Consider rate limiting when making multiple requests
4. Keep Valorant running while using the client
5. Handle authentication token refresh when needed
