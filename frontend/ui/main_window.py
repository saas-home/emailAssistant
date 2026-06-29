from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
from services.api_client import ApiClient

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
    
    def set_button_enabled(self,enabled):
        self.rewrite_button.setEnabled(enabled)
        self.grammar_button.setEnabled(enabled)
        self.professional_button.setEnabled(enabled)

    def rewrite_clicked(self):
        self.set_button_enabled(False)
        self.outputbox.setPlainText("Generating...")
        result = self.api_client.generate(
            action="rewrite",
            text="thjis is a sampel text with some erors."
        )
        self.outputbox.setPlainText(result["suggestion"][0])
        self.set_button_enabled(True)
    def grammar_clicked(self):
        print("grammar clicked!!")

    def professional_clicked(self):
        print("professional clicked!!")