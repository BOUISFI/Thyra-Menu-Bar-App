import logging
import os
import subprocess
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from background_thyra_scripts import Thyra


class ThyraApp:
    """The main application class for the There tray icon and menu."""

    def __init__(self):
        """Initialize the application."""
        # Show logs in Terminal
        logging.getLogger().setLevel(logging.INFO)

        # Get the current working directory
        cwd = os.getcwd()

        # Construct the absolute path to the resources
        self.resource_path = os.path.join(cwd, 'images')

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

    def create_menu(self):
        """Create the tray menu."""
        self.menu = QMenu()

        # Check if there-server is installed
        result = subprocess.run(["which", self.thyra.cmd_start_thyra], stdout=subprocess.PIPE)
        if result.stdout:
            # Add the "Start Thyra" action if there-server is installed
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
                self.thyra.start_thyra()
            except Exception as e:
                logging.error("Failed to start Thyra: %s", e)
                return
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
            self.thyra.stop_thyra()
        self.app.quit()

    def run(self):
        """Run the application."""
        # Set the resources using the function
        self.set_resources(self.resource_path)
        self.app.exec()


if __name__ == "__main__":
    app = ThyraApp()
    app.run()
