from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QListWidget, QTextEdit,
    QPushButton, QFileDialog, QMessageBox
)

from backend.main_ingest import ingest_video
from backend.reasoning.answer_engine import answer_question


# =========================
# BACKGROUND WORKER
# =========================
class VideoIngestWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        try:
            lesson_path = ingest_video(self.video_path)
            self.finished.emit(lesson_path)
        except Exception as e:
            self.error.emit(str(e))


# =========================
# MAIN DASHBOARD VIEW
# =========================
class DashboardView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        root = QHBoxLayout(self)

        # -------- LEFT PANEL --------
        left_panel = QVBoxLayout()
        lesson_label = QLabel("📘 Today’s Lesson")

        self.concept_list = QListWidget()
        self.concept_list.addItem("Upload a video to see concepts")

        left_panel.addWidget(lesson_label)
        left_panel.addWidget(self.concept_list)

        # -------- RIGHT PANEL --------
        right_panel = QVBoxLayout()

        upload_label = QLabel("🎥 Upload Today’s Class Video")
        self.upload_status = QLabel("Please upload today’s classroom video to begin.")

        self.upload_button = QPushButton("📂 Choose Video")
        self.upload_button.clicked.connect(self.upload_video)

        right_panel.addWidget(upload_label)
        right_panel.addWidget(self.upload_status)
        right_panel.addWidget(self.upload_button)
        right_panel.addSpacing(15)

        chat_label = QLabel("👩‍🏫 Ask Your AI Teacher")

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setPlaceholderText(
            "👋 Hello!\nUpload today’s class video first."
        )

        self.input_box = QTextEdit()
        self.input_box.setFixedHeight(60)
        self.input_box.setPlaceholderText("✏️ Type your question here...")

        self.send_button = QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.on_send_clicked)

        right_panel.addWidget(chat_label)
        right_panel.addWidget(self.chat_box)
        right_panel.addWidget(self.input_box)
        right_panel.addWidget(self.send_button)

        root.addLayout(left_panel, 2)
        root.addLayout(right_panel, 5)

    # =========================
    # VIDEO UPLOAD
    # =========================
    def upload_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Classroom Video",
            "",
            "Video Files (*.mp4 *.mkv *.avi)"
        )

        if not file_path:
            return

        self.upload_status.setText("⏳ AI is learning from today’s class...")
        self.upload_button.setEnabled(False)
        self.send_button.setEnabled(False)

        self.thread = QThread()
        self.worker = VideoIngestWorker(file_path)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_ingest_finished)
        self.worker.error.connect(self.on_ingest_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_ingest_finished(self, lesson_path):
        self.upload_status.setText("✅ Lesson is ready!")
        self.upload_button.setEnabled(True)
        self.send_button.setEnabled(True)

        self.chat_box.clear()
        self.chat_box.append(
            "👩‍🏫 AI Teacher:\n"
            "I have learned from today’s class.\n"
            "You can now ask me questions!"
        )

        self.concept_list.clear()
        self.concept_list.addItem("Lesson loaded successfully")

    def on_ingest_error(self, message):
        self.upload_status.setText("❌ Failed to read video")
        self.upload_button.setEnabled(True)

        QMessageBox.critical(
            self,
            "Error",
            "Something went wrong while reading the video."
        )

    # =========================
    # CHAT
    # =========================
    def on_send_clicked(self):
        question = self.input_box.toPlainText().strip()
        if not question:
            return

        self.chat_box.append(f"🧒 You:\n{question}\n")
        self.input_box.clear()

        answer = answer_question(question)
        self.chat_box.append(f"👩‍🏫 AI Teacher:\n{answer}\n")
