from voiceos.configuration import Configuration
from voiceos.api_client import ApiClient
from voiceos.api.agents_api import AgentsApi
from voiceos.api.conversations_api import ConversationsApi
from voiceos.api.phone_numbers_api import PhoneNumbersApi

class VoiceOS:
    def __init__(self, api_key):
        self.configuration = Configuration(
            host="https://api.voiceos.io",
        )

        self.client = ApiClient(
            configuration=self.configuration,
            header_name="Authorization",
            header_value="Bearer " + api_key,
        )

        self.agents = AgentsApi(self.client)

        self.conversations = ConversationsApi(self.client)

        self.phone_numbers = PhoneNumbersApi(self.client)