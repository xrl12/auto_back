from PyQt5.QtWidgets import QWidget, QLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal


class FileSelectionWidget(QWidget):
    dir_selected = pyqtSignal(str)  # 新定义一

    def __init__(self, parent, label_font, btn_button, layout: QLayout, debug: bool, choice_dir: str = None):
        super().__init__(parent)
        label = QLabel(label_font)
        self.button = QPushButton(btn_button, self)
        # self.line_edit = QLineEdit()
        # self.line_edit.setReadOnly(True)

        layout.addRow(label, self.button)
        self.button.clicked.connect(self.select_file)
        if debug and not choice_dir:
            raise RuntimeError('当debug是true 当时候choice_dir是必填当')
        if debug:
            self.__choice_dir(choice_dir)

    def select_file(self):
        choice_dir = QFileDialog.getExistingDirectory(self, 'Select File')
        if choice_dir:
            self.button.setText(choice_dir)
        self.dir_selected.emit(choice_dir)

    def __choice_dir(self, choice_dir):
        self.button.setText(choice_dir)
        self.dir_selected.emit(choice_dir)
