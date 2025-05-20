import pjsua2 as pj
import asyncio

class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    def on_incoming_call(self, call):
        print("Входящий вызов от", call.info().remote_uri)
        call.answer(200)

class SipClient:
    def __init__(self):
        self.lib = pj.Lib()
        self.lib.init()
        self.lib.create_transport(pj.TransportType.UDP)
        self.lib.start()

    def register(self, sip_server, username, password):
        acc_cfg = pj.AccountConfig()
        acc_cfg.idUri = f"sip:{username}@{sip_server}"
        acc_cfg.regConfig.registrarUri = f"sip:{sip_server}"
        acc_cfg.sipConfig.authCreds.append(pj.AuthCredInfo("digest", "*", username, 0, password))
        account = pj.Account()
        account.create(acc_cfg)
        account.set_callback(MyAccountCallback(account))

async def main():
    client = SipClient()
    client.register("sip.example.com", "user", "password")
    await asyncio.sleep(3600)  # Держим приложение активным

if __name__ == "__main__":
    asyncio.run(main())