import hashlib
import os
import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QWidget, QTableWidgetItem, QFileDialog, QHeaderView


def calculate_hash(file_path):
    hasher = hashlib.md5()

    with open(file_path, "rb") as file:
        buffer = file.read()
        hasher.update(buffer)

    return hasher.hexdigest()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pyFileChecker")
        self.setGeometry(0, 0, 750, 500)
        self.center_window()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Group Box 1: File Input
        file_groupbox = QGroupBox("File Input")
        file_layout = QVBoxLayout()

        self.file_path_label = QLabel("File Path:")
        self.file_path_edit = QLineEdit()
        self.browse_file_button = QPushButton("Browse File")
        self.browse_file_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_file_button)

        file_groupbox.setLayout(file_layout)

        # Group Box 2: Directory Input
        directory_groupbox = QGroupBox("Directory Input")
        directory_layout = QVBoxLayout()

        self.directory_path_label = QLabel("Directory Path:")
        self.directory_path_edit = QLineEdit()
        self.browse_directory_button = QPushButton("Browse Directory")
        self.browse_directory_button.clicked.connect(self.browse_directory)

        directory_layout.addWidget(self.directory_path_label)
        directory_layout.addWidget(self.directory_path_edit)
        directory_layout.addWidget(self.browse_directory_button)

        directory_groupbox.setLayout(directory_layout)

        # Group Box 3: File Details Table
        details_groupbox = QGroupBox("File Details")
        details_layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["File Name", "Hash", "Location"])

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        details_layout.addWidget(self.table_widget)

        details_groupbox.setLayout(details_layout)

        main_layout.addWidget(file_groupbox)
        main_layout.addWidget(directory_groupbox)
        main_layout.addWidget(details_groupbox)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")

        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                self.update_table(file_path)

    def browse_directory(self):
        directory_dialog = QFileDialog()
        directory_dialog.setFileMode(QFileDialog.FileMode.Directory)

        if directory_dialog.exec():
            directory_path = directory_dialog.selectedFiles()[0]
            self.update_table(directory_path)

    def update_table(self, path):
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            file_hash = self.calculate_hash(path)

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(file_name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(file_hash))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(path))
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    file_hash = self.calculate_hash(full_path)

                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    self.table_widget.setItem(row_position, 0, QTableWidgetItem(file_name))
                    self.table_widget.setItem(row_position, 1, QTableWidgetItem(file_hash))
                    self.table_widget.setItem(row_position, 2, QTableWidgetItem(full_path))

    def calculate_hash(self, file_path):
        hasher = hashlib.md5()

        with open(file_path, "rb") as file:
            buffer = file.read()
            hasher.update(buffer)

        return hasher.hexdigest()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
