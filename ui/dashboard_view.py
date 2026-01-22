from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QPushButton, QListWidget, QLineEdit,
    QFileDialog, QMessageBox, QTextEdit, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
import os
import json

from ui.chat_widget import ChatWidget


class VideoProcessorThread(QThread):
    """Background thread for processing videos"""
    finished = Signal(bool)
    error_msg = Signal(str)
    
    def __init__(self, video_path, dashboard):
        super().__init__()
        self.video_path = video_path
        self.dashboard = dashboard
    
    def run(self):
        """Run in background thread"""
        try:
            from backend.ingest.main_ingest import ingest_lesson
            
            print(f"🎬 Starting video processing: {self.video_path}")
            lesson_path = ingest_lesson(self.video_path)
            
            if lesson_path:
                print(f"✅ Video processed successfully: {lesson_path}")
                self.finished.emit(True)
            else:
                print("❌ Video processing returned None")
                self.error_msg.emit("Video processing failed - Check if video has audio")
                self.finished.emit(False)
                
        except Exception as e:
            print(f"❌ Error in video processing: {str(e)}")
            self.error_msg.emit(f"Error: {str(e)}")
            self.finished.emit(False)


class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_lesson_path = None
        self.processor_thread = None

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ================= TOP SECTION - LESSON INFO =================
        top_section = QFrame()
        top_section.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border-radius: 12px;
                border: 2px solid #2A2A2A;
            }
        """)
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(20, 15, 20, 15)
        top_layout.setSpacing(20)

        # Left - Lesson Status
        lesson_label = QLabel("📚 Today's Lesson:")
        lesson_font = QFont()
        lesson_font.setPointSize(12)
        lesson_font.setBold(True)
        lesson_label.setFont(lesson_font)

        self.lesson_status = QLabel("No lesson uploaded")
        status_font = QFont()
        status_font.setPointSize(11)
        self.lesson_status.setFont(status_font)
        self.lesson_status.setStyleSheet("color: #9CA3AF;")

        # Right - Upload Button
        self.upload_btn = QPushButton("📁 Upload Video")
        self.upload_btn.setFixedHeight(40)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.upload_btn.clicked.connect(self.choose_video)

        left_info = QVBoxLayout()
        left_info.addWidget(lesson_label)
        left_info.addWidget(self.lesson_status)

        top_layout.addLayout(left_info, 1)
        top_layout.addWidget(self.upload_btn)

        main_layout.addWidget(top_section)

        # ================= MIDDLE SECTION - CONCEPTS =================
        concepts_section = QFrame()
        concepts_section.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border-radius: 12px;
                border: 2px solid #2A2A2A;
            }
        """)
        concepts_layout = QVBoxLayout(concepts_section)
        concepts_layout.setContentsMargins(20, 15, 20, 15)

        concepts_title = QLabel("🎯 Topics to Learn:")
        concepts_font = QFont()
        concepts_font.setPointSize(12)
        concepts_font.setBold(True)
        concepts_title.setFont(concepts_font)

        self.concept_list = QListWidget()
        self.concept_list.setFixedHeight(100)
        self.concept_list.addItem("Upload a video to see topics")
        self.concept_list.setStyleSheet("""
            QListWidget {
                background-color: #0A0A0A;
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                color: #E5E7EB;
            }
            QListWidget::item {
                padding: 8px;
            }
        """)

        concepts_layout.addWidget(concepts_title)
        concepts_layout.addWidget(self.concept_list)

        main_layout.addWidget(concepts_section)

        # ================= BOTTOM SECTION - TABS =================
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #2A2A2A;
                border-radius: 12px;
                background-color: #1A1A1A;
            }
            QTabBar::tab {
                background-color: #0A0A0A;
                border: 1px solid #2A2A2A;
                padding: 12px 20px;
                border-radius: 8px 8px 0 0;
                font-weight: bold;
                font-size: 12px;
                color: #9CA3AF;
            }
            QTabBar::tab:selected {
                background-color: #1A1A1A;
                border: 2px solid #3B82F6;
                color: #E5E7EB;
            }
        """)

        # -------- TAB 1: Chat --------
        chat_tab = QWidget()
        chat_layout = QVBoxLayout(chat_tab)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_widget = ChatWidget()
        self.chat_widget.setEnabled(False)

        chat_layout.addWidget(self.chat_widget)

        # -------- TAB 2: Tasks --------
        tasks_tab = QWidget()
        tasks_layout = QVBoxLayout(tasks_tab)
        tasks_layout.setContentsMargins(15, 15, 15, 15)
        tasks_layout.setSpacing(12)

        tasks_header = QLabel("✅ My Learning Tasks")
        tasks_header_font = QFont()
        tasks_header_font.setPointSize(12)
        tasks_header_font.setBold(True)
        tasks_header.setFont(tasks_header_font)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #0A0A0A;
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                color: #E5E7EB;
            }
            QListWidget::item {
                padding: 12px;
                margin: 4px;
            }
            QListWidget::item:selected {
                background-color: #1E40AF;
            }
        """)

        task_input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("✍️  Add a new task...")
        self.task_input.setFixedHeight(40)

        self.add_task_btn = QPushButton("➕ Add")
        self.add_task_btn.setFixedWidth(80)
        self.add_task_btn.setFixedHeight(40)
        self.add_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.add_task_btn.clicked.connect(self.add_task)

        task_input_layout.addWidget(self.task_input)
        task_input_layout.addWidget(self.add_task_btn)

        tasks_layout.addWidget(tasks_header)
        tasks_layout.addWidget(self.task_list)
        tasks_layout.addLayout(task_input_layout)

        # -------- TAB 3: Notes --------
        notes_tab = QWidget()
        notes_layout = QVBoxLayout(notes_tab)
        notes_layout.setContentsMargins(15, 15, 15, 15)
        notes_layout.setSpacing(12)

        notes_header = QLabel("📝 My Study Notes")
        notes_header_font = QFont()
        notes_header_font.setPointSize(12)
        notes_header_font.setBold(True)
        notes_header.setFont(notes_header_font)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("📖 Write your notes here...")
        self.notes_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0A0A0A;
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                color: #E5E7EB;
            }
        """)

        self.save_notes_btn = QPushButton("💾 Save Notes")
        self.save_notes_btn.setFixedHeight(40)
        self.save_notes_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        self.save_notes_btn.clicked.connect(self.save_notes)

        notes_layout.addWidget(notes_header)
        notes_layout.addWidget(self.notes_edit)
        notes_layout.addWidget(self.save_notes_btn)

        # Add tabs
        tabs.addTab(chat_tab, "💬 Chat with AI")
        tabs.addTab(tasks_tab, "📋 My Tasks")
        tabs.addTab(notes_tab, "📝 My Notes")

        main_layout.addWidget(tabs)

        # Set background
        self.setStyleSheet("background-color: #0A0A0A;")

    # ================= ACTIONS =================

    def choose_video(self):
        """Open file dialog to choose video"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a Class Video",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.mov)"
        )

        if not file_path:
            return

        self.current_lesson_path = file_path
        file_name = os.path.basename(file_path)
        
        self.lesson_status.setText(f"⏳ Processing: {file_name}...")
        self.concept_list.clear()
        self.concept_list.addItem("🎬 Extracting audio...")
        self.concept_list.addItem("🗣️ Transcribing...")
        self.concept_list.addItem("🏷️ Finding topics...")
        
        self.upload_btn.setEnabled(False)
        
        self.processor_thread = VideoProcessorThread(file_path, self)
        self.processor_thread.finished.connect(self.on_processing_finished)
        self.processor_thread.error_msg.connect(self.on_processing_error)
        self.processor_thread.start()

    def on_processing_finished(self, success):
        """Called when video processing is done"""
        self.upload_btn.setEnabled(True)
        
        if success:
            self.load_lesson_concepts()
            QMessageBox.information(
                self,
                "🎉 Lesson Ready!",
                "Your lesson is ready!\nStart asking questions to your AI teacher! 🤖"
            )
        else:
            self.lesson_status.setText("❌ Processing failed - Use a video with audio")

    def on_processing_error(self, error_msg):
        """Called if there's an error during processing"""
        self.upload_btn.setEnabled(True)
        QMessageBox.critical(
            self,
            "❌ Error",
            f"Could not process video:\n{error_msg}\n\nMake sure your video has audio!"
        )
        self.lesson_status.setText("❌ Upload failed")

    def load_lesson_concepts(self):
        """Load concepts from structured lesson"""
        self.concept_list.clear()

        try:
            if not self.current_lesson_path:
                self.concept_list.addItem("No lesson loaded")
                return

            base_name = os.path.splitext(
                os.path.basename(self.current_lesson_path)
            )[0]
            
            lesson_path = f"backend/data/lessons/{base_name}_structured.json"
            
            if not os.path.exists(lesson_path):
                lesson_path = "backend/data/lessons/lecture_structured.json"
            
            if not os.path.exists(lesson_path):
                self.concept_list.addItem("⏳ Still processing...")
                return

            with open(lesson_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            file_name = os.path.basename(self.current_lesson_path)
            self.lesson_status.setText(f"✅ {file_name}")

            self.chat_widget.lesson_context = data
            self.chat_widget.setEnabled(True)

            concepts = data.get("concepts", [])
            
            if concepts:
                for concept in concepts:
                    concept_name = concept.get('name', 'Unknown')
                    self.concept_list.addItem(f"🎯 {concept_name}")
            else:
                self.concept_list.addItem("• No topics found")

        except Exception as e:
            self.concept_list.addItem(f"❌ Error: {str(e)}")

    def save_notes(self):
        """Save notes to file"""
        notes_text = self.notes_edit.toPlainText()
        
        if not notes_text.strip():
            QMessageBox.warning(self, "Empty", "Write some notes first! 📝")
            return
        
        os.makedirs("backend/data", exist_ok=True)
        
        try:
            with open("backend/data/notes.txt", "w", encoding="utf-8") as f:
                f.write(notes_text)
            QMessageBox.information(self, "✅ Saved!", "Your notes are saved! 🎉")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save: {e}")

    def add_task(self):
        """Add task to list"""
        task = self.task_input.text().strip()
        if not task:
            QMessageBox.warning(self, "Empty", "Write a task first! ✍️")
            return
        self.task_list.addItem(f"☑️  {task}")
        self.task_input.clear()