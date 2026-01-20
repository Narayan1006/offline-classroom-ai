from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class HomeView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("SikshaLokam")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")

        subtitle = QLabel("Offline AI Classroom Assistant")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px; color: #555;")

        start_button = QPushButton("Start Learning")
        start_button.setFixedWidth(220)
        start_button.setStyleSheet("padding: 12px; font-size: 16px;")
        start_button.clicked.connect(self.main_window.go_to_dashboard)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(start_button)
