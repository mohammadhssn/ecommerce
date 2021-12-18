import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AWGc8pZUN6fis34zFrhRmbQexwvlJwzZD_goAiWdPZrx_iuaUkkQhN1uVg5Rk4rhtFi-kKPu_zQ7zjb1"
        self.client_secret = "EKex8lre0lgBZjhaH6WvDVRa5QtRn5NklL_ZGA6PaUA2rzM2wCUwnQ8XQUq9tiJ1yZwnd6me7L7lSGED"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
