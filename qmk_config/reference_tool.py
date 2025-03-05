import sys
from PyQt5.QtWidgets import *
from pathlib import Path
from document_ingester import ingest
from document_parser import doc_parser
from tag_generator import generate
import os
import logging
from func_lib import logger_setup
from datetime import datetime

class ProcessTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.PLANT = 1  # Default value
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # File selection button
        self.select_button = QPushButton('Select FS document', self)
        self.select_button.clicked.connect(self.showFileDialog)
        layout.addWidget(self.select_button)

        # Label to show selected file
        self.file_label = QLabel('No file selected', self)
        layout.addWidget(self.file_label)

        # button for running ingester function on selected file
        self.ingest_button = QPushButton('Run Ingest on document', self)
        self.ingest_button.clicked.connect(self.runIngestOnFileWithShow)
        layout.addWidget(self.ingest_button)
        # button for running parser function on selected file
        self.parser_button = QPushButton('Run parser on document', self)
        self.parser_button.clicked.connect(self.runParserOnFile)
        layout.addWidget(self.parser_button)

        self.generate_tabs_button = QPushButton('Generate tags', self)
        self.generate_tabs_button.clicked.connect(self.run_generator)
        layout.addWidget(self.generate_tabs_button)

        # int input for limit unit instance option
        lui_form_layout = QFormLayout()
        self.lui_input = QSpinBox(self)
        self.lui_input.setValue(1)
        lui_form_layout.addRow('Limit unit instance', self.lui_input)

        self.select_all_unit_instances = QCheckBox('', self)
        self.select_all_unit_instances.setChecked(False)
        lui_form_layout.addRow('All unit instances', self.select_all_unit_instances)
        layout.addLayout(lui_form_layout)

        # Show metrics from ingest function
        self.ingest_metric_table = QTableWidget()
        layout.addWidget(self.ingest_metric_table)

        # Dropdown for selecting plant number
        self.plant_dropdown = QComboBox(self)
        self.plant_dropdown.addItems([str(i) for i in range(1, 11)])  # Numbers 1-10
        self.plant_dropdown.setCurrentIndex(0)  # Default is 1 (index 0)
        self.plant_dropdown.currentIndexChanged.connect(self.updatePlant)
        layout.addWidget(QLabel('Select Plant Number:'))
        layout.addWidget(self.plant_dropdown)

        ## Disable tqdm loading
        self.disable_tqdm = QCheckBox('', self)
        self.disable_tqdm.setChecked(True)
        lui_form_layout.addRow('Disable tqdm', self.disable_tqdm)
        layout.addLayout(lui_form_layout)


        self.fname = ''

    def showFileDialog(self):
        logger = logging.getLogger('dev_tool_logger')
        raw_document_path = f'{os.getcwd()}/data/{self.PLANT}/raw/documents/'
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', raw_document_path, 'All Files (*)')
        if self.fname:
            self.file_label.setText(f'Selected file: {Path(self.fname)}')
            logger.info(f'Selected file: {Path(self.fname)}',extra = {'error_code':'0000'})
    def updatePlant(self):
        logger = logging.getLogger('dev_tool_logger')

        """Update PLANT variable when dropdown selection changes."""
        self.PLANT = int(self.plant_dropdown.currentText())
        logger.info(f"Selected Plant: {self.PLANT}",extra = {'error_code':'0000'})

    def run_generator(self):
        generate()

    def runIngestOnFileWithShow(self):
        logger = logging.getLogger('dev_tool_logger')

        if self.fname:
            start_time = time.time()
            self.doct_dict = ingest(Path(self.fname))
            end_time = time.time()

            execution_time = end_time - start_time

            logger.info(f'ingested file {Path(self.fname).name}  (Ingest time: {execution_time:.2f} seconds)',extra = {'error_code':'0000'})
            meta_data = self.doct_dict['meta_data']
            self.ingest_metric_table.setColumnCount(2)
            self.ingest_metric_table.setRowCount(len(meta_data))
            self.ingest_metric_table.setHorizontalHeaderLabels(['Key', 'Value'])
            for row, (key, value) in enumerate(meta_data.items()):
                self.ingest_metric_table.setItem(row, 0, QTableWidgetItem(str(key)))
                self.ingest_metric_table.setItem(row, 1, QTableWidgetItem(str(value)))
            self.ingest_metric_table.resizeColumnsToContents()
        else:
            logger.info('No file selected, please select file',extra = {'error_code':'0000'})

    def runParserOnFile(self):
        logger = logging.getLogger('dev_tool_logger')

        if self.fname:
            if self.select_all_unit_instances.checkState():
                self.lui_input.setValue(0)

            args = Namespace(file_path=[self.fname],
                             limit_unit_instance = [self.lui_input.value()],
                             data_input_folder   = [os.getcwd()+f'/data/{self.PLANT}/raw/documents/'],
                             data_output_folder  = [os.getcwd()+f'/data/{self.PLANT}/intermediate/intermediate_tags'],
                             disable_tqdm        = [self.disable_tqdm.checkState()]
                             )

            start_time = time.time()
            doc_parser(args)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f'Parsed file {Path(self.fname).name}  (Parse time: {execution_time:.2f} seconds)',extra = {'error_code':'0000'})

class XML_explore_tab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # File selection button
        self.select_button = QPushButton('Select intermediate tag', self)
        self.select_button.clicked.connect(self.showFileDialog)
        layout.addWidget(self.select_button)

        # Label to show selected file
        self.file_label = QLabel('No file selected', self)
        layout.addWidget(self.file_label)

def showFileDialog(self):
        raw_document_path = f'{os.getcwd()}/data/{self.PLANT}/intermediate/intermediate_tags'

        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', raw_document_path, 'All Files (*)')
        if self.fname:
            self.file_label.setText(f'Selected file: {Path(self.fname).name}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Viewer')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create and add the Input tab
        process_tab = ProcessTab()

        self.tab_widget.addTab(process_tab, "Process")

        # Create and add the Output tab
        explore_tab = XML_explore_tab()
        self.tab_widget.addTab(explore_tab, "Explore")

def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    LOG_FILE_NAME = os.getcwd()+ '/logs/dev_tool/'+datetime.now().strftime(r'dev_tool_%Y_%m_%d_%H_%M_%S.log')
    logger_setup(log_file_name=LOG_FILE_NAME,
                    logger_name='dev_tool_logger')
    logger = logging.getLogger('dev_tool_logger')

    main()