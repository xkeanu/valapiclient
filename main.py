# main.py

from valapiclient.client import ValorantClient

def main():
    client = ValorantClient()
    api = client.valclient()
    print(f'Player: {api.get_current_player()}')

    #print(api.pregame.lock_pregame_agent("e370fa57-4757-3604-3648-499e1f642d3f"))

    print(api.coregame.get_current_match_id())

    #print(f'Party: {api.party.get_current_party()}')

    print(api.coregame.get_current_match_info(api.coregame.get_current_match_id()))

    #print(api.coregame.get_current_match_loadout(api.coregame.get_current_match_id()))

    #print(api.coregame.leave_current_match())

    #print(api.party.join_queue())
    #print(api.party.get_current_party())

    #print(api.store.get_store_offers())

    #print(api.pvp.get_account_xp(api.get_current_player_puuid()))
    #print(api.pvp.get_player_loadout(api.get_current_player_puuid()))

    print(api.pvp.get_player_name('bb1d3d06-65bd-5636-84cd-65af319be821'))

    #print(api.pregame.dodge_pregame_match())
if __name__ == "__main__":
    main()
