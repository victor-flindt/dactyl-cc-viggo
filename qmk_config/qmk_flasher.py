from pathlib import Path
import os
import sys
from PyQt5 import QtGui
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMK Flasher')
        self.setGeometry(100, 100, 800, 600)  # Make the window larger to allow more space

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a widget for the buttons and file label
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)

        # Set up the Ctrl+W shortcut to close the application
        close_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)

        # File selection button
        self.select_button = QPushButton('Select qmk hex file', self)
        self.select_button.setFixedHeight(30)  # Make the button smaller
        self.select_button.clicked.connect(self.showFileDialog)
        button_layout.addWidget(self.select_button)

        # Label to show selected file
        self.file_label = QLabel('No file selected', self)
        self.file_label.setFixedHeight(20)  # Make the label smaller
        button_layout.addWidget(self.file_label)

        self.ingest_button = QPushButton('Flash board', self)
        self.ingest_button.setFixedHeight(30)  # Make the button smaller
        self.ingest_button.clicked.connect(self.run_flasher)
        button_layout.addWidget(self.ingest_button)

        # Add the button widget to the layout
        layout.addWidget(button_widget)

        # Embed the web engine view and allow it to take up the remaining space
        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl("https://config.qmk.fm/#/handwired/dactyl_cc/LAYOUT"))
        layout.addWidget(self.web_view)

    def showFileDialog(self):
        raw_document_path = f'{os.getcwd()}/qmk_config/'

        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', raw_document_path, 'All Files (*)')
        if self.fname:
            self.file_label.setText(f'Selected file: {Path(self.fname).name}')

    def run_flasher(self) -> None:
        os.system(f"avrdude -p m32u4 -c avr109 -P /dev/ttyACM0 -U flash:w:{self.fname}:i")


def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__': 
    main()
