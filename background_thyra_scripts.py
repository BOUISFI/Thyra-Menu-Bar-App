import logging
import webbrowser
import background_process
import time


class Thyra:
    """
    Class for representing the Thyra system and its associated methods.
    """

    CONST_WALLET_LINK = "http://my.massa/thyra/wallet/index.html"
    CONST_WEBSITE_CREATOR_LINK = "http://my.massa/thyra/websiteCreator/index.html"
    CONST_CMD_THYRA = "thyra-server"

    def __init__(self, cmd_start_thyra=CONST_CMD_THYRA, wallet_link=None, website_creator_link=None):
        """
        Initializes the Thyra system with the specified parameters.

        Args:
            Coded using ternary operator
            cmd_start_thyra (str, optional): The command to start the Thyra server. Defaults to CONST_CMD_THYRA.
            wallet_link (str, optional): The link to the wallet. Defaults to CONST_WALLET_LINK.
            website_creator_link (str, optional): The link to the website creator. Defaults to CONST_WEBSITE_CREATOR_LINK.
        """
        self.cmd_start_thyra = cmd_start_thyra or self.CONST_CMD_THYRA
        self.wallet = wallet_link or self.CONST_WALLET_LINK
        self.website_creator = website_creator_link or self.CONST_WEBSITE_CREATOR_LINK
        self.thyra = background_process.Process(cmd_start_thyra)

    def launch_wallet(self):
        """
        Launches the wallet in the default web browser.
        """
        try:
            webbrowser.open(self.wallet)
        except Exception as e:
            logging.error("Error while launching wallet: {}".format(e))

    def launch_website_creator(self):
        """
        Launches the website creator in the default web browser.
        """
        try:
            webbrowser.open(self.website_creator)
        except Exception as e:
            logging.error("Error launching website creator: {}".format(e))

    def start_thyra(self):
        """
        Starts the Thyra server.
        """
        self.thyra.start()
        time.sleep(1)

    def stop_thyra(self):
        """
        Stops the Thyra server.
        """
        self.thyra.stop()
