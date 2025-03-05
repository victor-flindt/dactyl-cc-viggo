from pathlib import Path
import subprocess
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMK Flasher')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Set up the Ctrl+W shortcut to close the application
        close_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)

        # File selection button
        self.select_button = QPushButton('Select qmk hex file', self)
        self.select_button.clicked.connect(self.showFileDialog)
        layout.addWidget(self.select_button)

        # Label to show selected file
        self.file_label = QLabel('No file selected', self)
        layout.addWidget(self.file_label)

        self.ingest_button = QPushButton('Flash board', self)
        self.ingest_button.clicked.connect(self.run_flasher)
        layout.addWidget(self.ingest_button)

    def showFileDialog(self):
        raw_document_path = f'{os.getcwd()}/qmk_config/'

        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', raw_document_path, 'All Files (*)')
        if self.fname:
            self.file_label.setText(f'Selected file: {Path(self.fname).name}')

    def run_flasher(self) -> None:
        print(self.fname)

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__': 
    main()
    