import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.getcwd(), relative_path)


def load_styles(app):
    style_path = resource_path("ui/styles.qss")
    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)

    # 🔥 THIS LINE MAKES DARK THEME WORK
    app.setStyle("Fusion")

    load_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
