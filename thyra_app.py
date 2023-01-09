import logging
import os
import shutil
import subprocess
import sys
import time

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from utils.background_thyra_scripts import Thyra


class ThyraApp:
    """The main application class for the There tray icon and menu."""

    def __init__(self):
        """Initialize the application."""

        # Get the current working directory
        if getattr(sys, 'frozen', False):
            self.cwd = sys._MEIPASS
        else:
            self.cwd = os.getcwd()

        # Expand the '~' character to the user's home directory
        home_dir = os.path.expanduser('~')

        # Get the .config folder
        self.config_dir = os.path.join(home_dir, '.config')

        # Set up logging
        self.setup_logging()

        # Set up the PATH variable
        self.setup_path()

        # Construct the absolute path to the resources
        self.resource_path = os.path.join(self.cwd, 'images')

        # Create the application and tray icon
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.tray = QSystemTrayIcon()
        # Set the tray icon
        self.tray.setIcon(QIcon(os.path.join(self.resource_path, 'logo.png')))
        self.tray.setVisible(True)
        # Track if Thyra is running
        self.thyra_running = False

        # Create the Thyra object
        self.thyra = Thyra()

        # Create the menu
        self.create_menu()

        # Add the "Quit" action
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.stop_thyra_and_quit)
        self.menu.addAction(self.quit)

    def setup_logging(self):
        """Set up logging for the application."""

        # Construct the absolute path to the log file
        log_file = os.path.join(self.config_dir, 'ThyraApp.log')

        # Create a file handler for the log file
        file_handler = logging.FileHandler(log_file)

        # Set the log level for the file handler
        file_handler.setLevel(logging.INFO)

        # Create a stream handler for the console
        console_handler = logging.StreamHandler()

        # Set the log level for the console handler
        console_handler.setLevel(logging.INFO)

        # Create a log formatter
        formatter = logging.Formatter('%(levelname)s: %(message)s')

        # Set the formatter for the file handler
        file_handler.setFormatter(formatter)

        # Set the formatter for the console handler
        console_handler.setFormatter(formatter)

        # Get the root logger
        logger = logging.getLogger()

        # Add the file handler to the root logger
        logger.addHandler(file_handler)

        # Add the console handler to the root logger
        logger.addHandler(console_handler)

    def setup_path(self):
        """Set up the PATH variable for the application."""

        # Set the timeout to 5 seconds
        timeout = 5

        # Run the script which write  the PATH variable to the file in the .config folder
        process = subprocess.run(["python3", os.path.join(self.cwd, 'path.py')], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        file_path = os.path.join(self.config_dir, 'path.txt')
        # Wait for the file to be created, with a timeout of 5 seconds
        start_time = time.time()
        while not file_path:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                # Timeout reached, giving up
                break
            time.sleep(1)

        # If File Created set the Env Path
        if file_path:
            with open(file_path, 'r') as f:
                path = f.read()
                os.environ['PATH'] = path

    def create_menu(self):
        """Create the tray menu."""
        self.menu = QMenu()

        # Check if there-server is installed
        result = shutil.which("thyra-server")
        if result is None or result == '':
            logging.error("cannot find thyra-server path. please run as sudo, and check if path.txt is well created "
                          "in your .conf.")
        else:
            logging.info("The thyra-server is installed and will be launched from the path {}.".format(result))
            # Add the "Start Thyra" action if thyra-server is installed
            self.thyra_action = QAction("Start Thyra")
            self.thyra_action.setCheckable(True)
            self.thyra_action.triggered.connect(self.toggle_thyra)
            self.menu.addAction(self.thyra_action)

        # Add the menu to the tray
        self.tray.setContextMenu(self.menu)

        # Add the "Wallet" action
        self.wallet_action = QAction("Wallet")
        self.wallet_action.triggered.connect(self.thyra.launch_wallet)
        self.menu.addAction(self.wallet_action)

        # Add the "Website Creator" action
        self.web_onchain_action = QAction("Web Onchain")
        self.web_onchain_action.triggered.connect(self.thyra.launch_website_creator)
        self.menu.addAction(self.web_onchain_action)

    def toggle_thyra(self):
        if self.thyra_action.isChecked():
            # Start Thyra
            try:
                thyra_logs_ok = self.thyra.start_thyra()
            except Exception as e:
                logging.error("Failed to start Thyra: %s", e)
                return
            if not thyra_logs_ok:
                logging.error("Failed to start Thyra, please check the logs")
            else:
                self.thyra_action.setIcon(QIcon(os.path.join(self.resource_path, 'off_icon.png')))
                self.thyra_action.setText("Stop Thyra")
                self.thyra_running = True

        else:
            # Stop Thyra
            try:
                self.thyra.stop_thyra()
            except Exception as e:
                logging.error("Failed to stop Thyra: %s", e)
                return
            self.thyra_action.setIcon(QIcon(os.path.join(self.resource_path, 'on_icon.png')))
            self.thyra_action.setText("Start Thyra")
            self.thyra_running = False

    def set_resources(self, resource_path):
        # Set the icons for the actions
        self.wallet_action.setIcon(QIcon(os.path.join(resource_path, 'wallet.png')))
        self.web_onchain_action.setIcon(QIcon(os.path.join(resource_path, 'website.png')))

        if hasattr(self, 'thyra_action'):
            # Set the icon for the "Start Thyra" action if it exists
            self.thyra_action.setIcon(QIcon(os.path.join(resource_path, 'on_icon.png')))

            # Set the icon for the "Start Thyra" action if it exists
            self.quit.setIcon(QIcon(os.path.join(resource_path, 'close')))

    def stop_thyra_and_quit(self):
        if self.thyra_running:
            self.thyra.quit_thyra()
        self.app.quit()

    def run(self):
        """Run the application."""
        # Set the resources using the function
        self.set_resources(self.resource_path)
        self.app.exec()


if __name__ == "__main__":
    app = ThyraApp()
    app.run()
