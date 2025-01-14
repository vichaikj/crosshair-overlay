# To convert that file into a .exe:
#     pip install pyinstaller
#     python -m PyInstaller --icon=C:\Users\JP\Documents\scripts\crosshair\crosshair.ico --onefile --noconsole --add-data "C:\Users\JP\Documents\scripts\crosshair\crosshair.ico;." C:\Users\JP\Documents\scripts\crosshair\crosshair.py


import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QSystemTrayIcon


# Icon used for the tray
ICO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crosshair.ico")

# add a small offset if the center of the crosshair is off
OFFSET = False
# Choose the option by updating the number below (1 or 2)
SELECTED_OPTION = 2


# Define the options dictionary
options = {
    1: {"line_length": 12, "hole_size": 6, "thickness": 3},  # Option 1
    2: {"line_length": 16, "hole_size": 8, "thickness": 4}   # Option 2
}


# Extract the values based on the selected option
line_length = options[SELECTED_OPTION]["line_length"]
hole_size = options[SELECTED_OPTION]["hole_size"]
thickness = options[SELECTED_OPTION]["thickness"]


class CrosshairOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dynamically get screen resolution
        screen = QApplication.primaryScreen()
        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()

        # Window properties
        self.setWindowTitle("Transparent Crosshair Overlay")
        self.setGeometry(0, 0, self.screen_width, self.screen_height)  # Full-screen overlay
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enables transparency
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # Ignore mouse events
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)  # No borders, stays on top

        # Show the overlay
        self.show()

    def paintEvent(self, event):
        transparency = 0.8  # Transparency (percent)
        outline_thickness = thickness + 2  # Outline is slightly thicker than the main crosshair
        painter = QPainter(self)

        # Calculate the center of the screen
        offset_value = 1 if OFFSET else 0  # Re-adjustment because slightly off-centered in-game
        center_x = (self.screen_width // 2) - offset_value
        center_y = (self.screen_height // 2) - offset_value

        # Draw the dark green outline
        outline_pen = QPen(QColor(0, 100, 0, round(255 * transparency)))  # Dark green color
        outline_pen.setWidth(outline_thickness)
        painter.setPen(outline_pen)

        # Draw the horizontal outline
        painter.drawLine(center_x - line_length, center_y, center_x - hole_size, center_y)  # Left part
        painter.drawLine(center_x + hole_size, center_y, center_x + line_length, center_y)  # Right part

        # Draw the vertical outline
        painter.drawLine(center_x, center_y - line_length, center_x, center_y - hole_size)  # Top part
        painter.drawLine(center_x, center_y + hole_size, center_x, center_y + line_length)  # Bottom part

        # Draw the main crosshair
        pen = QPen(QColor(0, 255, 0, round(255 * transparency)))  # Bright green color
        pen.setWidth(thickness)
        painter.setPen(pen)

        # Draw the horizontal crosshair
        painter.drawLine(center_x - line_length, center_y, center_x - hole_size, center_y)  # Left part
        painter.drawLine(center_x + hole_size, center_y, center_x + line_length, center_y)  # Right part

        # Draw the vertical crosshair
        painter.drawLine(center_x, center_y - line_length, center_x, center_y - hole_size)  # Top part
        painter.drawLine(center_x, center_y + hole_size, center_x, center_y + line_length)  # Bottom part


class TrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Crosshair Overlay")
        menu = QMenu(parent)

        exit_action = QAction("Exit", parent)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set up the crosshair overlay
    overlay = CrosshairOverlay()

    # Set up the system tray icon
    tray_icon = TrayIcon(QIcon(ICO_PATH), overlay)
    tray_icon.show()

    sys.exit(app.exec_())
