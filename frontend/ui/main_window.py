from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
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

        layout.addWidget(self.rewrite_button)
        layout.addWidget(self.grammar_button)
        layout.addWidget(self.professional_button)

        self.rewrite_button.clicked.connect(self.rewrite_clicked)
        self.grammar_button.clicked.connect(self.grammar_clicked)
        self.professional_button.clicked.connect(self.professional_clicked)

        self.setLayout(layout)

    def rewrite_clicked(self):
        result = self.api_client.generate(
            action="rewrite",
            text="thjis is a sampel text with some erors."
        )
        print(result)

    def grammar_clicked(self):
        print("grammar clicked!!")

    def professional_clicked(self):
        print("professional clicked!!")