# To convert that file into a .exe:
#     pip install pyinstaller
#     python -m PyInstaller --icon=C:\Users\JP\Documents\GitHub\crosshair-overlay\crosshair.ico --onefile --noconsole --add-data "C:\Users\JP\Documents\GitHub\crosshair-overlay\crosshair.ico;." C:\Users\JP\Documents\GitHub\crosshair-overlay\crosshair.py


import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QSystemTrayIcon


# Icon used for the tray
ICO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crosshair.ico")

# Add a small offset if the center of the crosshair is off
OFFSET = False

# Default option
CROSSHAIR_SIZE = "medium"
CROSSHAIR_COLOR = "green"

# Size definitions
sizes = {
    "small": {"line_length": 8, "hole_size": 4, "thickness": 2, "transparency": 0.8},
    "medium": {"line_length": 12, "hole_size": 6, "thickness": 3, "transparency": 0.8},
    "large": {"line_length": 16, "hole_size": 8, "thickness": 4, "transparency": 0.8},
}

# Color definitions
colors = {
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 150, 255),
    "white": (255, 255, 255),
}


def apply_size(option):
    """Update global drawing parameters"""
    global CROSSHAIR_SIZE, line_length, hole_size, thickness, transparency
    CROSSHAIR_SIZE = option
    line_length = sizes[option]["line_length"]
    hole_size = sizes[option]["hole_size"]
    thickness = sizes[option]["thickness"]
    transparency = sizes[option]["transparency"]


def apply_color(name):
    """Update global color values"""
    global CROSSHAIR_COLOR, color_r, color_g, color_b
    CROSSHAIR_COLOR = name
    color_r, color_g, color_b = colors[name]


# Default apply
apply_size(CROSSHAIR_SIZE)
apply_color(CROSSHAIR_COLOR)


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

    def refresh(self):
        """Force a redraw when settings change"""
        self.update()

    def paintEvent(self, event):
        outline_thickness = thickness + 2  # Outline is slightly thicker than the main crosshair
        painter = QPainter(self)

        # Calculate the center of the screen
        offset_value = 1 if OFFSET else 0  # Re-adjustment because slightly off-centered in-game
        center_x = (self.screen_width // 2) - offset_value
        center_y = (self.screen_height // 2) - offset_value

        # Draw the outline (darkened version of current color)
        outline_pen = QPen(QColor(color_r // 4, color_g // 4, color_b // 4, round(255 * transparency)))
        outline_pen.setWidth(outline_thickness)
        painter.setPen(outline_pen)

        # Draw the horizontal outline
        painter.drawLine(center_x - line_length, center_y, center_x - hole_size, center_y)  # Left part
        painter.drawLine(center_x + hole_size, center_y, center_x + line_length, center_y)  # Right part

        # Draw the vertical outline
        painter.drawLine(center_x, center_y - line_length, center_x, center_y - hole_size)  # Top part
        painter.drawLine(center_x, center_y + hole_size, center_x, center_y + line_length)  # Bottom part

        # Draw the main crosshair
        pen = QPen(QColor(color_r, color_g, color_b, round(255 * transparency)))
        pen.setWidth(thickness)
        painter.setPen(pen)

        # Draw the horizontal crosshair
        painter.drawLine(center_x - line_length, center_y, center_x - hole_size, center_y)  # Left part
        painter.drawLine(center_x + hole_size, center_y, center_x + line_length, center_y)  # Right part

        # Draw the vertical crosshair
        painter.drawLine(center_x, center_y - line_length, center_x, center_y - hole_size)  # Top part
        painter.drawLine(center_x, center_y + hole_size, center_x, center_y + line_length)  # Bottom part


class TrayIcon(QSystemTrayIcon):
    def __init__(self, icon, overlay, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Crosshair Overlay")
        self.overlay = overlay

        # Context menu
        menu = QMenu(parent)

        # ---- CREATE MENUS ----
        self.size_menu = self._create_menu("Size", sizes.keys(), self.switch_size, CROSSHAIR_SIZE)
        self.color_menu = self._create_menu("Color", colors.keys(), self.switch_color, CROSSHAIR_COLOR)

        menu.addMenu(self.size_menu)
        menu.addMenu(self.color_menu)

        # ---- EXIT ----
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def _create_menu(self, title, options_list, callback, selected_option):
        """Helper to create a QMenu with checkable actions."""
        menu = QMenu(title)
        for opt in options_list:
            action = QAction(opt.capitalize(), checkable=True)
            action.setChecked(opt == selected_option)
            action.triggered.connect(lambda _, o=opt: callback(o))
            menu.addAction(action)
            # store as attribute for easy access
            setattr(self, f"{opt}_action", action)
        return menu

    def switch_size(self, size_option):
        apply_size(size_option)
        for size in sizes.keys():
            getattr(self, f"{size}_action").setChecked(size == size_option)
        self.overlay.refresh()

    def switch_color(self, color_option):
        apply_color(color_option)
        for color in colors.keys():
            getattr(self, f"{color}_action").setChecked(color == color_option)
        self.overlay.refresh()

    def exit_app(self):
        QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set up the crosshair overlay
    overlay = CrosshairOverlay()
    tray_icon = TrayIcon(QIcon(ICO_PATH), overlay)
    tray_icon.show()

    sys.exit(app.exec_())
