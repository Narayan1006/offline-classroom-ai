from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt

from ui.home_view import HomeView
from ui.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)


        self.setWindowTitle("Siksha Saathi – Offline AI Teaching Assistant")

        self.setMinimumSize(1100, 700)

        # ===== CENTRAL CONTAINER =====
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        central_widget.setAutoFillBackground(True)
        self.setCentralWidget(central_widget)


        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        self.header = QWidget()
        self.header.setObjectName("HeaderWidget")
        self.header.setFixedHeight(60)

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        self.title_label = QLabel("🧠 Siksha Saathi")
        self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.welcome_label = QLabel("👋 Hello!")
        self.welcome_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.welcome_label)

        # ===== STACKED SCREENS =====
        self.stack = QStackedWidget()

        self.home_view = HomeView(self)
        self.dashboard_view = DashboardView(self)

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.dashboard_view)

        self.stack.setCurrentWidget(self.home_view)

        # ===== FOOTER =====
        self.footer = QWidget()
        self.footer.setObjectName("FooterWidget")
        self.footer.setFixedHeight(50)

        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(self.go_back)

        self.progress_label = QLabel("🟢⚪⚪⚪⚪")
        self.progress_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        footer_layout.addWidget(self.back_button)
        footer_layout.addStretch()
        footer_layout.addWidget(self.progress_label)

        # ===== ASSEMBLE LAYOUT =====
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.stack)
        main_layout.addWidget(self.footer)

    # ===== NAVIGATION =====
    def go_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_view)
        self.progress_label.setText("🟢🟢⚪⚪⚪")

    def go_back(self):
        self.stack.setCurrentWidget(self.home_view)
        self.progress_label.setText("🟢⚪⚪⚪⚪")
