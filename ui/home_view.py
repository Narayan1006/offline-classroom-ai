from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


class FeatureCard(QFrame):
    """Colorful card for feature display"""
    def __init__(self, emoji, title, description, color):
        super().__init__()
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 16px;
                border: none;
            }}
        """)
        
        self.setFixedHeight(180)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Emoji - Large
        emoji_label = QLabel(emoji)
        emoji_font = QFont()
        emoji_font.setPointSize(48)
        emoji_label.setFont(emoji_font)
        emoji_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        
        # Description
        desc_label = QLabel(description)
        desc_font = QFont()
        desc_font.setPointSize(11)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        layout.addWidget(emoji_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()


class HomeView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Main layout with scroll
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top section - Welcome
        top_section = QWidget()
        top_layout = QVBoxLayout(top_section)
        top_layout.setContentsMargins(30, 40, 30, 30)
        top_layout.setSpacing(15)
        
        # Main Title
        title = QLabel("🧠 Siksha Saathi")
        title_font = QFont()
        title_font.setPointSize(42)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #F9FAFB;")
        
        # Subtitle
        subtitle = QLabel("Your Personal AI Learning Buddy! 🎓")
        subtitle_font = QFont()
        subtitle_font.setPointSize(16)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #9CA3AF;")
        
        # Tagline
        tagline = QLabel("Learn better. Ask questions. Grow smarter!")
        tagline_font = QFont()
        tagline_font.setPointSize(12)
        tagline_font.setItalic(True)
        tagline.setFont(tagline_font)
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #6B7280;")
        
        top_layout.addWidget(title)
        top_layout.addWidget(subtitle)
        top_layout.addWidget(tagline)
        
        # Middle section - Features
        middle_section = QWidget()
        middle_layout = QVBoxLayout(middle_section)
        middle_layout.setContentsMargins(30, 20, 30, 20)
        middle_layout.setSpacing(20)
        
        # Feature label
        features_title = QLabel("✨ What You Can Do:")
        features_title_font = QFont()
        features_title_font.setPointSize(14)
        features_title_font.setBold(True)
        features_title.setFont(features_title_font)
        features_title.setStyleSheet("color: #F9FAFB;")
        
        # Features in 3 columns
        features_grid = QHBoxLayout()
        features_grid.setSpacing(20)
        
        # Feature 1: Video & Chat
        card1 = FeatureCard(
            "🎬",
            "Upload & Learn",
            "Upload your class videos and chat with your AI teacher!",
            "#991B1B"  # Dark Red
        )
        
        # Feature 2: Todo
        card2 = FeatureCard(
            "✅",
            "My Tasks",
            "Keep track of learning goals and homework tasks!",
            "#064E3B"  # Dark Teal
        )
        
        # Feature 3: Notes
        card3 = FeatureCard(
            "📝",
            "My Notes",
            "Take notes while learning and save them forever!",
            "#1E3A8A"  # Dark Blue
        )
        
        features_grid.addWidget(card1)
        features_grid.addWidget(card2)
        features_grid.addWidget(card3)
        
        middle_layout.addWidget(features_title)
        middle_layout.addLayout(features_grid)
        
        # Bottom section - CTA Button
        bottom_section = QWidget()
        bottom_layout = QVBoxLayout(bottom_section)
        bottom_layout.setContentsMargins(30, 30, 30, 50)
        bottom_layout.setSpacing(15)
        
        # Motivational message
        motivation = QLabel(
            "Ready to become a learning superstar? 🌟"
        )
        motivation_font = QFont()
        motivation_font.setPointSize(13)
        motivation_font.setBold(True)
        motivation.setFont(motivation_font)
        motivation.setAlignment(Qt.AlignCenter)
        motivation.setStyleSheet("color: #3B82F6;")
        
        # Start button
        start_button = QPushButton("🚀 Start Learning Now!")
        start_button.setFixedHeight(50)
        start_button.setFixedWidth(280)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        start_button.clicked.connect(self.main_window.go_to_dashboard)
        
        bottom_layout.addWidget(motivation)
        bottom_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        bottom_layout.addStretch()
        
        # Assemble everything
        main_layout.addWidget(top_section)
        main_layout.addWidget(middle_section)
        main_layout.addWidget(bottom_section)
        
        # Set background color
        self.setStyleSheet("background-color: #0A0A0A;")