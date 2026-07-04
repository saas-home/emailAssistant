from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt6.QtCore import QThread

from services.api_client import ApiClient
from worker.api_worker import ApiWorker


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.api_client = ApiClient()

        self.setWindowTitle("AI Writing Assistant :)")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.rewrite_button = QPushButton("Rewrite")
        self.grammar_button = QPushButton("Correct Grammar")
        self.professional_button = QPushButton("Make It Professional")

        self.outputbox = QPlainTextEdit()
        self.outputbox.setReadOnly(True)

        layout.addWidget(self.rewrite_button)
        layout.addWidget(self.grammar_button)
        layout.addWidget(self.professional_button)
        layout.addWidget(self.outputbox)

        self.rewrite_button.clicked.connect(self.rewrite_clicked)
        self.grammar_button.clicked.connect(self.grammar_clicked)
        self.professional_button.clicked.connect(self.professional_clicked)

        self.setLayout(layout)

    def set_buttons_enabled(self, enabled):
        self.rewrite_button.setEnabled(enabled)
        self.grammar_button.setEnabled(enabled)
        self.professional_button.setEnabled(enabled)

    def rewrite_clicked(self):
        self.start_generation("rewrite")

    def grammar_clicked(self):
        self.start_generation("grammar")

    def professional_clicked(self):
        self.start_generation("professional")

    def start_generation(self, action):
        text = "thjis is a sampel text with some erors."

        self.set_buttons_enabled(False)
        self.outputbox.setPlainText("Generating...")

        self.thread = QThread()

        self.worker = ApiWorker(
            self.api_client,
            action,
            text
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.on_generation_success)
        self.worker.error.connect(self.on_generation_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_generation_success(self, result):
        self.outputbox.setPlainText(result["suggestion"][0])
        self.set_buttons_enabled(True)

    def on_generation_error(self, error):
        self.outputbox.setPlainText(error)
        self.set_buttons_enabled(True)

