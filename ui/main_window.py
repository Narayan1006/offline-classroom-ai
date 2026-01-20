from PySide6.QtWidgets import QMainWindow, QStackedWidget
from ui.home_view import HomeView
from ui.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SikshaLokam – Offline AI Classroom")
        self.setMinimumSize(1100, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_view = HomeView(self)
        self.dashboard_view = DashboardView(self)

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.dashboard_view)

        self.stack.setCurrentWidget(self.home_view)

    def go_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_view)
