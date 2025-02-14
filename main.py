import sys
import time
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import yt_dlp


class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url.split("?si=")[0]

    def run(self):
        try:
            output_path = os.path.join(os.path.expanduser("~"), "Downloads", "%(title)s.%(ext)s")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'progress_hooks': [self.hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                if 'entries' in info:  # Check if it's a playlist
                    urls = [entry['url'] for entry in info['entries'] if 'url' in entry]
                else:
                    urls = [self.url]

            for index, video_url in enumerate(urls, start=1):
                try:
                    ydl_opts['progress_hooks'] = [self.hook]
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                except Exception as e:
                    self.error.emit(str(e))
                self.progress.emit(int((index / len(urls)) * 100))

            self.finished.emit("Download completed successfully!")
        except Exception as e:
            self.error.emit(str(e))

    def hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            self.progress.emit(int(percent))


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("musiFy")
        self.setWindowIcon(QIcon("icon.png"))  # Set application icon
        self.resize(500, 250)
        self.centerWindow()

        # Apply dark theme and increase element sizes
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #3E3E3E;
                border: 2px solid #5A5A5A;
                color: #FFFFFF;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #5A5A5A;
                border: 2px solid #777777;
                color: #FFFFFF;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QProgressBar {
                background-color: #3E3E3E;
                border: 2px solid #5A5A5A;
                color: #FFFFFF;
                font-size: 14px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #00AA00;
            }
        """)

        self.layout = QVBoxLayout()

        self.inputField = QLineEdit(self)
        self.inputField.setPlaceholderText("Enter YouTube URL here")
        self.layout.addWidget(self.inputField)

        self.startButton = QPushButton("Download Audio", self)
        self.startButton.clicked.connect(self.startProcess)
        self.layout.addWidget(self.startButton)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progressBar)

        self.setLayout(self.layout)

    def centerWindow(self):
        screen = QApplication.primaryScreen().geometry()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen.center())
        self.move(window_rect.topLeft())

    def startProcess(self):
        url = self.inputField.text().strip()
        if not url:
            QMessageBox.critical(self, "Error", "Please enter a valid YouTube URL.")
            return

        self.startButton.setEnabled(False)  # Disable button during process
        self.worker = WorkerThread(url)
        self.worker.progress.connect(self.updateProgress)
        self.worker.finished.connect(self.processFinished)
        self.worker.error.connect(self.processError)
        self.worker.start()

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def processFinished(self, message):
        self.startButton.setEnabled(True)  # Re-enable button after process
        QMessageBox.information(self, "Success", message)

    def processError(self, error_message):
        self.startButton.setEnabled(True)
        QMessageBox.critical(self, "Download Error", f"An error occurred: {error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
