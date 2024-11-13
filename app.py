import sys
import markdown
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QTextEdit, QLabel, QFileDialog, QMessageBox, QSplitter, QMenu, QPushButton, QScrollArea
)
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt, QSize

class MarkdownPreviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Preview - Enhanced UI with Emoji Support")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("icon.png"))

        self.markdown_editor = QTextEdit()
        self.markdown_editor.setPlaceholderText("Write your Markdown here... 📝")
        self.markdown_editor.setFont(QFont("Arial", 14))
        self.markdown_editor.textChanged.connect(self.update_preview)
        self.markdown_editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)  # Connect scroll signal

        self.markdown_preview = QLabel()
        self.markdown_preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.markdown_preview.setWordWrap(True)
        self.markdown_preview.setFont(QFont("Arial", 14))
        self.preview_scroll_area = QScrollArea()
        self.preview_scroll_area.setWidgetResizable(True)
        self.preview_scroll_area.setWidget(self.markdown_preview)

        self.menu_button = QPushButton("Menu")
        self.menu_button.setStyleSheet("padding: 8px; border-radius: 5px;")
        self.menu_button.setFixedWidth(80)

        self.menu = QMenu()
        open_action = self.menu.addAction("Open")
        open_action.triggered.connect(self.open_file)

        save_action = self.menu.addAction("Save")
        save_action.triggered.connect(self.save_file)

        toggle_preview_action = self.menu.addAction("Toggle Preview")
        toggle_preview_action.triggered.connect(self.toggle_preview)

        self.menu_button.setMenu(self.menu)

        self.emoji_button = QPushButton("😊 Emoji")
        self.emoji_button.setStyleSheet("padding: 8px; border-radius: 5px;")
        self.emoji_button.clicked.connect(self.open_emoji_dialog)

        self.create_central_widget()

    def create_central_widget(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.markdown_editor)
        self.splitter.addWidget(self.preview_scroll_area)
        self.splitter.setSizes([400, 400])  

        # Button layout on top
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.menu_button)
        button_layout.addWidget(self.emoji_button)
        
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.splitter)

        self.setCentralWidget(central_widget)

    def update_preview(self):
        """Convert Markdown to HTML and display it in the preview pane."""
        markdown_text = self.markdown_editor.toPlainText()
        html = markdown.markdown(markdown_text)
        self.markdown_preview.setText(html)

    def sync_scroll(self):
        """Sync the scrolling position between the editor and preview."""
        editor_scroll = self.markdown_editor.verticalScrollBar()
        preview_scroll = self.preview_scroll_area.verticalScrollBar()

        scroll_ratio = editor_scroll.value() / editor_scroll.maximum() if editor_scroll.maximum() > 0 else 0
        preview_scroll.setValue(int(scroll_ratio * preview_scroll.maximum()))

    def open_file(self):
        """Open a Markdown file and display its contents in the editor."""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Markdown files (*.md)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "r") as file:
                self.markdown_editor.setText(file.read())
            self.update_preview()

    def save_file(self):
        """Save the contents of the editor to a Markdown file."""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Markdown files (*.md)")
        file_dialog.setDefaultSuffix("md")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "w") as file:
                file.write(self.markdown_editor.toPlainText())
            QMessageBox.information(self, "Save Successful", "Markdown file saved successfully.")

    def toggle_preview(self):
        """Toggle visibility of the preview panel."""
        if self.preview_scroll_area.isHidden():
            self.preview_scroll_area.show()
            self.menu_button.setText("Hide Preview")
        else:
            self.preview_scroll_area.hide()
            self.menu_button.setText("Show Preview")

    def open_emoji_dialog(self):
        """Open an emoji selection dialog and insert selected emoji into the editor."""
        emoji_list = ["😀", "😂", "😊", "😍", "😎", "😢", "🤔", "👍", "🎉", "🔥"]
        emoji_menu = QMenu(self)
        for emoji in emoji_list:
            emoji_action = QAction(emoji, self)
            emoji_action.triggered.connect(lambda _, e=emoji: self.insert_emoji(e))
            emoji_menu.addAction(emoji_action)
        
        emoji_menu.exec(self.emoji_button.mapToGlobal(self.emoji_button.rect().bottomLeft()))

    def insert_emoji(self, emoji):
        """Insert an emoji at the current cursor position in the editor."""
        cursor = self.markdown_editor.textCursor()
        cursor.insertText(emoji)
        self.markdown_editor.setTextCursor(cursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownPreviewApp()
    window.show()
    sys.exit(app.exec())
