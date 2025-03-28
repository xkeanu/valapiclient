# main.py
import time
import random

#from docutils.parsers.rst.directives import positive_int

from valapiclient.client import ValorantClient

def main():
    client = ValorantClient()
    api = client.valclient()
    #print(f'Player: {api.get_current_player()}')

    #print(api.pregame.get_current_pregame())
    #print(f'Player: {api.get_current_player()}')

    #print(api.pregame.get_current_pregame())

    #print(api.pregame.lock_pregame_agent("e370fa57-4757-3604-3648-499e1f642d3f"))

    #print(api.coregame.get_current_match_id())
    #print(api.coregame.get_current_match_id())

    #print(f'Party: {api.party.get_current_party()}')

    #print(api.coregame.get_current_match_info(api.coregame.get_current_match_id()))
    #print(api.coregame.get_current_match_info(api.coregame.get_current_match_id()))

    #print(api.coregame.get_current_match_loadout(api.coregame.get_current_match_id()))

    #print(api.coregame.leave_current_match())

    #print(api.party.join_queue())
    #print(api.party.get_current_party())

    #print(api.store.get_store_offers())

    #print(api.pvp.get_account_xp(api.get_current_player_puuid()))
    #print(api.pvp.get_player_loadout(api.get_current_player_puuid()))

    print(api.pvp.get_player_name('914fd2ca-2614-5322-bddd-0c22a1fa1b00'))

    #print(api.pregame.dodge_pregame_match())

    #print(api.party.party_invite('zockie#9104'))

    #print(api.party.party_invite('Riot VoiDzz#RIOT'))

    #print(api.pregame.select_pregame_agent(''))

    #print(api.coregame.leave_current_match())

    # agent_uuids = [
    #     "5f8d3a7f-467b-97f3-062c-13acf203c006",  # Breach
    #     "f94c3b30-42be-e959-889c-5aa313dba261",  # Raze
    #     "6f2a04ca-43e0-be17-7f36-b3908627744d",  # Skye
    #     "117ed9e3-49f3-6512-3ccf-0cada7e3823b",  # Cypher
    #     "320b2a48-4d9b-a075-30f1-1f93a9b638fa",  # Sova
    #     "1e58de9c-4950-5125-93e9-a0aee9f98746",  # Killjoy
    #     "707eab51-4836-f488-046a-cda6bf494859",  # Viper
    #     "eb93336a-449b-9c1b-0a54-a891f7921d69",  # Phoenix
    #     "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",  # Brimstone
    #     "7f94d92c-4234-0a36-9646-3a87eb8b5c89",  # Yoru
    #     "569fdd95-4d10-43ab-ca70-79becc718b46",  # Sage
    #     "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",  # Reyna
    #     "8e253930-4c05-31dd-1b6c-968525494517",  # Omen
    #     "add6443a-41bd-e414-f6ad-e58d267f4e95"  # Jett
    # ]
    #
    # for _ in range(10):
    #     selected_agent_uuid = random.choice(agent_uuids)
    #     response = api.pregame.select_pregame_agent(selected_agent_uuid)
    #     print(response)
    #     time.sleep(0.05)
    #
    # final_agent_uuid = random.choice(agent_uuids)
    # final_response = api.pregame.select_pregame_agent(final_agent_uuid)
    # print(f"Final Agent Selected: {final_response}")

    #print(api.pvp.get_player_name("fda97db4-1791-5b75-a892-e1543ba46a8d"))
    #print(api.pvp.get_player_mmr("fda97db4-1791-5b75-a892-e1543ba46a8d"))
    #print(api.coregame.get_current_match_info(api.coregame.get_current_match_id()))

    #print(api.pregame.dodge_pregame_match())
    #print(api.get_current_player_puuid())

    #print(api.pvp.get_player_mmr("044ac0bb-10b0-5533-84a0-51f74fe8923a"))

if __name__ == "__main__":
    main()
