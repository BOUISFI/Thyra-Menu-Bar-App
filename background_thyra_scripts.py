import webbrowser
import background_process
import time

CONST_WALLET_LINK = "http://my.massa/thyra/wallet/index.html"
CONST_WEBSITE_CREATOR_LINK = "http://my.massa/thyra/websiteCreator/index.html"
CONST_CMD_THYRA = "thyra-server"


class Thyra(object):
    def __init__(self, cmd_start_thyra="", wallet_link=None, website_creator_link=None):
        self.cmd_start_thyra = cmd_start_thyra if cmd_start_thyra is not None else CONST_CMD_THYRA
        self.wallet = wallet_link if wallet_link is not None else CONST_WALLET_LINK
        self.website_creator = website_creator_link if website_creator_link is not None else CONST_WEBSITE_CREATOR_LINK
        self.thyra = background_process.Process(cmd_start_thyra)

    def launch_wallet(self):
        webbrowser.open(self.wallet)

    def launch_website_creator(self):
        webbrowser.open(self.website_creator)

    def start_thyra(self):
        self.thyra.start_process()
        time.sleep(1)

    def stop_thyra(self):
        self.thyra.stop_process()
