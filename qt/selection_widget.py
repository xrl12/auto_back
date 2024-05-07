import sys
from PyQt5.QtWidgets import QApplication, QLayout, QLabel, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QWidget
from settings import TIME_UNIT
from utils.settings_utils import SettingsUtils


class SelectionWidget(QWidget):
    def __init__(self, item_list: list, parent=None):
        self.combobox = QComboBox()
        self.lineedit = QLineEdit()
        self.item_list = item_list
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # label_combo = QLabel('请选择间隔时间：')
        # layout.addWidget(label_combo)
        layout.setSpacing(0)
        for item in self.item_list:
            self.combobox.addItem(item[1], item[0])
        layout.addWidget(self.lineedit)
        layout.addWidget(self.combobox)
        self.setLayout(layout)

    def selectedOption(self):
        # 返回当前选中的选项的文本
        return self.combobox.currentData()

    def enteredText(self):
        # 返回文本输入框中的文本
        return self.lineedit.text()



