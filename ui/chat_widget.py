from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit
)
from PySide6.QtCore import Qt, Signal

# 🔥 BACKEND AI
from backend.reasoning.answer_engine import answer_question


# =========================================================
# CUSTOM INPUT: ENTER = SEND | SHIFT+ENTER = NEW LINE
# =========================================================
class ChatInput(QTextEdit):
    send_signal = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() & Qt.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.send_signal.emit()
        else:
            super().keyPressEvent(event)


# =========================================================
# CHAT BUBBLE
# =========================================================
class ChatBubble(QWidget):
    def __init__(self, text, is_user=False):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(420)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_user:
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #1E40AF;
                    color: white;
                    padding: 12px;
                    border-radius: 14px;
                    font-size: 14px;
                }
            """)
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #1A1A1A;
                    color: #E5E7EB;
                    padding: 12px;
                    border-radius: 14px;
                    font-size: 14px;
                    border: 1px solid #2A2A2A;
                }
            """)
            layout.addWidget(bubble)
            layout.addStretch()


# =========================================================
# CHAT WIDGET
# =========================================================
class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Optional: lesson context (can be injected later)
        self.lesson_context = None

        # Fixed height so UI doesn’t explode
        self.setMinimumHeight(420)
        self.setMaximumHeight(600)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # ---------- Scroll Area ----------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; }")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(6)
        self.chat_layout.addStretch()

        self.scroll.setWidget(self.chat_container)

        # ---------- INPUT (FIXED) ----------
        self.input_box = ChatInput()
        self.input_box.setFixedHeight(50)
        self.input_box.setPlaceholderText(
            "✍️ Ask questions only from today's lesson"
        )

        # ENTER KEY SENDS MESSAGE
        self.input_box.send_signal.connect(self.send_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedHeight(36)
        self.send_btn.clicked.connect(self.send_message)

        # ---------- Assemble ----------
        main_layout.addWidget(self.scroll,stretch=1)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.send_btn)

        # ---------- Welcome ----------
        self.add_ai_message(
            "👩‍🏫 Hello! I'm your AI teacher.\n"
            "Ask me about today's class."
        )

    # ================= HELPERS =================
    def add_user_message(self, text):
        bubble = ChatBubble(text, is_user=True)
        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1, bubble
        )
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def add_ai_message(self, text):
        bubble = ChatBubble(text, is_user=False)
        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1, bubble
        )
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    # ================= MAIN =================
    def send_message(self):
        question = self.input_box.toPlainText().strip()
        if not question:
            return

        self.add_user_message(question)
        self.input_box.clear()

        self.add_ai_message("🤔 Thinking...")

        try:
            answer = answer_question(question)
        except Exception as e:
            print("AI Error:", e)
            answer = "😔 I couldn’t answer that. Please try again."

        self.add_ai_message(answer)
