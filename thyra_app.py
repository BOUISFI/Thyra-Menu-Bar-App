
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from background_thyra_scripts import Thyra
import logging


# Show logs in Terminal
logging.getLogger().setLevel(logging.INFO)

# Instantiating Thyra
thyra = Thyra("thyra-server")

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("logo.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


# Create the menu
menu = QMenu()
action1 = QAction("Wallet")
action1.triggered.connect(thyra.launch_wallet)
menu.addAction(action1)

action2 = QAction("Website Creator")
action2.triggered.connect(thyra.launch_website_creator)
menu.addAction(action2)

action3 = QAction("Start Thyra")
action3.triggered.connect(thyra.start_thyra)
menu.addAction(action3)

action5 = QAction("Stop Thyra")
action5.triggered.connect(thyra.stop_thyra)
menu.addAction(action5)

quit = QAction("Quit")
quit.triggered.connect(thyra.stop_thyra)
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()