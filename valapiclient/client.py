from .local_api import ValClient

class ValorantClient:
    def __init__(self):
        print("Created by Keanu | Github: @xkeanu")
        self.api = ValClient.init_from_lockFile()

    def valclient(self):
        return self.api
