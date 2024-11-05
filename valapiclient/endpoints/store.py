class StoreEndpoints:
    def __init__(self, api):
        self.api = api

    def get_store_offers(self):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request("store/v1/offers/", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get store offers: {response.status_code if response else 'No response'}")
            return None

    def get_storefront(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"store/v2/storefront/{puuid}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get storefront: {response.status_code if response else 'No response'}")
            return None

    def get_wallet(self, puuid: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"store/v1/wallet/{puuid}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get wallet: {response.status_code if response else 'No response'}")
            return None

    def get_order(self, orderID: str):
        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        response = self.api.handle_pvp_request(f"store/v1/order/{orderID}", header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get order: {response.status_code if response else 'No response'}")
            return None

    def get_store_entitlements(self, puuid: str, itemType: str):
        item_type_dict = {
            "agents": "01bb38e1-da47-4e6a-9b3d-945fe4655707",
            "contracts": "f85cb6f7-33e5-4dc8-b609-ec7212301948",
            "sprays": "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475",
            "gun_buddies": "dd3bf334-87f3-40bd-b043-682a57a8dc3a",
            "cards": "3f296c07-64c3-494c-923b-fe692a4fa1bd",
            "skins": "e7c63390-eda7-46e0-bb7a-a6abdacd2433",
            "skin_variants": "3ad1b2b2-acdb-4524-852f-954a76ddae0a",
            "titles": "de7caa6b-adf7-4588-bbd1-143831e786c6"
        }

        if itemType not in item_type_dict:
            print(f"Invalid item type: {itemType}")
            return None

        header = self.api.base_pvp_header.copy()
        auth_info = self.api.get_auth_info()
        if not auth_info:
            print("Authentication info not available.")
            return None
        header["X-Riot-Entitlements-JWT"] = auth_info[1]
        prefix = self.api.get_pd_url()
        endpoint = f"store/v1/entitlements/{puuid}/{item_type_dict[itemType]}"
        response = self.api.handle_pvp_request(endpoint, header=header, prefix=prefix)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get store entitlements: {response.status_code if response else 'No response'}")
            return None
