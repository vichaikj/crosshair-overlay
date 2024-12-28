# To convert that file into a .exe:
#     pip install pyinstaller
#     python -m PyInstaller --icon=C:\Users\JP\Documents\scripts\crosshair\crosshair.ico --onefile --noconsole C:\Users\JP\Documents\scripts\crosshair\crosshair.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt


ICO_PATH = "C:/Users/JP/Documents/scripts/crosshair/crosshair.ico"


class CrosshairOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties (1440x2560 resolution)
        self.setWindowTitle("Transparent Crosshair Overlay")
        self.screen_width = 2560  # Width of the screen
        self.screen_height = 1440  # Height of the screen
        self.setGeometry(0, 0, self.screen_width, self.screen_height)  # Full-screen overlay
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enables transparency
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # Ignore mouse events
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)  # No borders, stays on top

        # Show the overlay
        self.show()

    def paintEvent(self, event):
        line_length = 12  # Dimensions of the "plus" sign (pixels in each direction from center)
        hole_size = 6  # Size of the "hole" at the center (in pixels)
        thickness = 3  # Line thickness
        transparency = 0.8  # Transparency (percent)
        outline_thickness = thickness + 2  # Outline is slightly thicker than the main crosshair
        painter = QPainter(self)

        # Calculate the center of the screen
        offset = 1  # Re-adjustment because slightly off-centered in-game
        center_x = (self.screen_width // 2) - offset
        center_y = (self.screen_height // 2) - offset

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
