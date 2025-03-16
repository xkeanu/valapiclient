from valapiclient import ValorantClient

def main():
    # Initialize the client
    print("Initializing Valorant client...")
    client = ValorantClient()
    api = client.valclient()

    # Get current player info
    player = api.get_current_player()
    print(f"\nCurrent player: {player['acct']['game_name']}#{player['acct']['tag_line']}")

    # Get party information
    party_id = api.party.get_current_party_id()
    if party_id:
        party = api.party.get_current_party()
        print(f"\nCurrent party ID: {party_id}")
        print(f"Party members: {len(party['Members'])}")
        
        # Print party members
        for member in party['Members']:
            print(f"- {member['PlayerIdentity']['GameName']}#{member['PlayerIdentity']['TagLine']}")
    else:
        print("\nNot currently in a party")

    # Get server status
    print("\nChecking server status...")
    ping_info = api.get_valorant_server_ping("EU-WEST")
    print(f"EU-WEST server:")
    print(f"- Average latency: {ping_info['avg_latency']}ms")
    print(f"- Packet loss: {ping_info['packet_loss']}%")

    # Get player MMR info
    print("\nFetching MMR information...")
    try:
        player_puuid = api.get_current_player_puuid()
        mmr_info = api.pvp.get_mmr(player_puuid)
        
        if mmr_info:
            latest_update = mmr_info.get('LatestCompetitiveUpdate', {})
            print("\nLatest competitive update:")
            print(f"- Rating before: {latest_update.get('RankedRatingBeforeUpdate', 'N/A')}")
            print(f"- Rating after: {latest_update.get('RankedRatingAfterUpdate', 'N/A')}")
            print(f"- Rating earned: {latest_update.get('RankedRatingEarned', 'N/A')}")
        else:
            print("\nNo MMR information available")
    except Exception as e:
        print(f"\nError fetching MMR information: {e}")

if __name__ == "__main__":
    main()
