from PyQt6.QtCore import QObject , pyqtSignal

class ApiWorker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self,api_client,action,text):
        super().__init__()
        self.api_client = api_client
        self.action = action
        self.text = text

    def run(self):
        try:
            result = self.api_client.generate(
                action=self.action,
                text=self.text
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))