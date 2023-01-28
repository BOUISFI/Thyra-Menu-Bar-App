import logging
import os
import platform
import shutil
import webbrowser
import utils.background_process


class Thyra:
    """
    Class for representing the Thyra system and its associated methods.
    """
    # Expand the '~' character to the user's home directory
    home_dir = os.path.expanduser('~')

    # Create the .config folder if it does not exist
    config_dir = os.path.join(home_dir, '.config')

    # Write the PATH variable to the file in the .config folder
    file_path = os.path.join(config_dir, 'path.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            path = f.read()
            os.environ['PATH'] = path

    # Get thyra-server filename
    THYRA_SERVER_FILENAME = ""        
    if platform.system() == "Windows":
        THYRA_SERVER_FILENAME = "thyra-server.exe"
    elif platform.system() == "Darwin":
        THYRA_SERVER_FILENAME = "thyra-server"

    CONST_WALLET_LINK = "http://my.massa/thyra/wallet/index.html"
    CONST_WEBSITE_CREATOR_LINK = "http://my.massa/thyra/websiteCreator/index.html"
    CONST_CMD_THYRA = os.path.join(os.path.expanduser("~"), THYRA_SERVER_FILENAME) or shutil.which("thyra-server")

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
        self.thyra = utils.background_process.Process(cmd_start_thyra)

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
        # Expected output when start thyra
        expected_output = ["", "",
        "Connected to node server https://test.massa.net/api/v2 (version TEST.18.0)",
        "Plugin Manager initialization",
        "Starting plugin 'Playground plugin' on port 4200",
        "Starting plugin 'Node Manager plugin' on port 4201",
        "Starting plugin 'Wallet plugin' on port 4202",
        "Serving thyra server at http://[::]:80",
        "Serving thyra server at https://[::]:443"
                           ]
        return self.thyra.start(1, expected_output)

    def stop_thyra(self):
        """
        Stops the Thyra server.
        """
        self.thyra.stop()

    def quit_thyra(self):
        """
        Stops the Thyra server.
        """
        self.thyra.quit()
