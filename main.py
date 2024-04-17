import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QPushButton, QLabel, QWidget, QFileDialog, \
    QHBoxLayout, QLayout, QMessageBox, QLineEdit

from PyQt5.QtCore import pyqtSignal, QThread
from watch_file import WatchFiles
from file_operate import FileOperate


class FileSelectionWidget(QWidget):
    dir_selected = pyqtSignal(str)  # 新定义一

    def __init__(self, parent, label_font, btn_button, layout: QLayout):
        super().__init__(parent)
        label = QLabel(label_font)
        self.button = QPushButton(btn_button, self)
        # self.line_edit = QLineEdit()
        # self.line_edit.setReadOnly(True)

        layout.addRow(label, self.button)
        self.button.clicked.connect(self.select_file)

    def select_file(self):
        choice_dir = QFileDialog.getExistingDirectory(self, 'Select File')
        if choice_dir:
            self.button.setText(choice_dir)
        self.dir_selected.emit(choice_dir)


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, watch_obj, source_file, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watch_obj = watch_obj
        self.source_file = source_file
        self.handler = handler

    def run(self):
        self.watch_obj.main(self.source_file, self.handler)

    def stop(self):
        self.watch_obj.stop()
        self.is_running = False


class MyWindow(QMainWindow):
    """
    如果继承了QMainWindow的类，则不能直接创建布局，需要使用QWidget去创建布局
    """

    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 150)  # 设置最小宽和高
        self.setMaximumSize(300, 150)  # 设置最大宽和高
        self.source_dir = ""
        self.target_dir = ""
        self.watch_file = WatchFiles
        self.source_file_selection_widget = None
        self.target_file_selection_widget = None
        self.work_thread = None
        self.setWindowTitle('自动备份app')
        self.create_form_layout()

    def create_form_layout(self):
        """
        创建一个表单布局
        :return:
        """
        # 创建一个组件（为了添加布局）
        widget = QWidget()
        self.setCentralWidget(widget)
        # 创建表单布局
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        self.source_file_selection_widget = FileSelectionWidget(self, '源目录', '选择监听目录', form_layout)
        self.target_file_selection_widget = FileSelectionWidget(self, '目标目录', '选择备份目录', form_layout)
        widget.setLayout(form_layout)
        # 监听选择文件信号
        self.source_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'source'))
        self.target_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'target'))

    def clear_choice_dir(self):
        """
        清除已经选择的目录
        :return:
        """
        if self.source_file_selection_widget:
            self.source_file_selection_widget.button.setText('选择监听目录')
        if self.target_file_selection_widget:
            self.target_file_selection_widget.button.setText('选择监听目录')

        self.source_dir = ''
        self.target_dir = ''

    def handle_selected_directory(self, directory, type_):
        """
        选择的目录
        :param directory:
        :param type_:
        :return:
        """
        type_map = {
            'source': "source_dir",
            'target': "target_dir"
        }
        attr = type_map.get(type_, None)
        if attr is None:
            raise ValueError('没有获取到当前类型')
        setattr(self, attr, directory)
        if self.source_dir:
            self.work_thread = WorkerThread(WatchFiles, self.source_dir, FileOperate())

        if self.source_dir and self.target_dir:
            # 判断源目录和目标目录是否一样
            if self.source_dir == self.target_dir:
                self.clear_choice_dir()
                QMessageBox.warning(self, 'Error', '源目录和目标目录一样，请重新选择')
                self.watch_file.stop()
            else:
                self.main()

    def main(self):
        """
        程序主函数，开始运行函数
        :return:
        """
        self.work_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
