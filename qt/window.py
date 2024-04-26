import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QPushButton, QLabel, QWidget, QFileDialog, \
    QLayout, QMessageBox

from PyQt5.QtCore import pyqtSignal, QThread
from watch.watch_file import WatchFiles
from file_operate.file_operate import FileOperate
from qt.file_select_on_widget import FileSelectionWidget
from thread import WorkerThread


class MyWindow(QMainWindow):
    """
    如果继承了QMainWindow的类，则不能直接创建布局，需要使用QWidget去创建布局
    """

    def __init__(self, debug=False):
        super().__init__()
        self.setMinimumSize(300, 150)  # 设置最小宽和高
        self.setMaximumSize(300, 150)  # 设置最大宽和高
        self.source_dir = ""
        self.target_dir = ""
        self.watch_file = WatchFiles
        self.source_file_selection_widget = None
        self.target_file_selection_widget = None
        self.work_thread = None
        self.debug = debug
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
        source_path = '/Users/xuruilong/Desktop/test_dir'
        target_path = '/Users/xuruilong/Desktop/test_dir1'
        self.source_file_selection_widget = FileSelectionWidget(self, '源目录', '选择监听目录', form_layout, self.debug,
                                                                source_path)
        self.target_file_selection_widget = FileSelectionWidget(self, '目标目录', '选择备份目录', form_layout,
                                                                self.debug, target_path)
        # button = QPushButton('关闭线程', self)
        # button.clicked.connect(self.stop_son_thread)
        #
        # start_btn = QPushButton('打开线程', self);
        # start_btn.clicked.connect(self.main)
        # form_layout.addWidget(start_btn)
        # form_layout.addWidget(button)
        widget.setLayout(form_layout)

        # 监听选择文件信号
        self.source_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'source'))
        self.target_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'target'))
        if self.debug:
            self.handle_selected_directory(source_path, 'source')
            self.handle_selected_directory(target_path, 'target')

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

        if self.source_dir and self.target_dir:
            if self.work_thread is not None:
                self.work_thread.stop()
                self.work_thread = None
            self.work_thread = WorkerThread(WatchFiles, self.source_dir, FileOperate(self.target_dir, self.source_dir))
            # 判断源目录和目标目录是否一样
            if self.source_dir == self.target_dir:
                self.clear_choice_dir()
                QMessageBox.warning(self, 'Error', '源目录和目标目录一样，请重新选择')
            else:
                self.main()

    def main(self):
        """
        程序主函数，开始运行函数
        :return:
        """
        # if self.work_thread.isRunning():
        #     self.work_thread.stop()
        # if self.work_thread is None:
        #     self.work_thread = WorkerThread(WatchFiles, self.source_dir, FileOperate(self.target_dir, self.source_dir))
        self.work_thread.start()

    # def stop_son_thread(self):
    #     print(self.work_thread.isRunning())
    #     # if self.work_thread.isRunning():
    #     self.work_thread.stop()
    #     self.work_thread.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow(False)
    window.show()
    sys.exit(app.exec_())
