import sys
from types import FunctionType
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QPushButton, QLabel, QWidget, QFileDialog, \
    QLayout, QMessageBox, QLineEdit, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QThread
from watch.watch_file import WatchFiles
from file_operate.file_operate import FileOperate
from qt.file_select_on_widget import FileSelectionWidget
from qt.auto_thread import WorkerThread
from settings import TIME_UNIT
from utils.settings_utils import SettingsUtils
from utils.valid_file_utils import ValidFileUtils


class MyWindow(QMainWindow):
    """
    如果继承了QMainWindow的类，则不能直接创建布局，需要使用QWidget去创建布局
    """

    def __init__(self, debug=False):
        super().__init__()
        self.setMinimumSize(300, 150)  # 设置最小宽和高
        self.setMaximumSize(300, 150)  # 设置最大宽和高
        self.source_dir = ""  # 源目录
        self.target_dir = ""  # 目标目录
        self.watch_file = WatchFiles
        self.source_file_selection_widget = None  # 选择源目录组件
        self.target_file_selection_widget = None  # 选择目标目录组件
        self.time_line_edit = None  # 编辑时间文本框
        self.work_thread = None  # 线程
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
        self.source_file_selection_widget = FileSelectionWidget(self, '源目录', self.create_q_btn(text='选择监听目录'),
                                                                form_layout, self.debug)
        self.target_file_selection_widget = FileSelectionWidget(self, '目标目录',
                                                                self.create_q_btn(text="选择备份目录"), form_layout,
                                                                self.debug)

        self.time_line_edit = self.create_q_line_edit("间隔时间，以毫秒为单位")
        form_layout.addRow(QLabel('间隔时间'), self.time_line_edit)
        box_layout = QHBoxLayout()
        box_layout.addWidget(self.create_q_btn(self.start, '开始'))
        box_layout.addWidget(self.create_q_btn(self.stop, '停止'))
        form_layout.addRow(QLabel('操作按钮'), box_layout)
        widget.setLayout(form_layout)

        # 监听选择文件信号
        self.source_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'source'))
        self.target_file_selection_widget.dir_selected.connect(lambda x: self.handle_selected_directory(x, 'target'))

    @staticmethod
    def create_q_line_edit(placeholder, default_val="10") -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setText(default_val)
        return line_edit

    def create_q_btn(self, click_method=None, text=None):
        """
        :param click_method: 按钮的点击事件
        :param text: 按钮的文本
        :return:
        """
        btn = QPushButton(text, self)
        if callable(click_method):
            btn.clicked.connect(click_method)
        return btn

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

    def create_message(self, message, type_='Error'):
        return QMessageBox.warning(self, type_, message)

    def start(self):
        """
        程序主函数，开始运行函数
        :return:
        """
        if not self.source_dir:
            return self.create_message("请选择源目录")
        elif not self.target_dir:
            return self.create_message("请选择目标目录")
        elif self.work_thread is not None:
            return self.create_message("已经在监听目录")
        elif self.source_dir == self.target_dir:
            self.clear_choice_dir()
            return self.create_message("源目录和目标目录一样，请重新选择")
        elif not ValidFileUtils.check_time_edit(self.time_line_edit.text()):
            return self.create_message("请使用2*2*1或者10格式")
        WatchFiles.sleet_time = eval(self.time_line_edit.text())
        self.work_thread = WorkerThread(WatchFiles, self.source_dir, FileOperate(self.target_dir, self.source_dir))
        self.create_message("开始成功", 'Success')
        self.work_thread.start()

    def stop(self):
        if not self.source_dir or not self.target_dir:
            return False
        elif self.work_thread is None:
            return False
        self.work_thread.stop()
        self.work_thread = None
        self.create_message("停止成功", 'Success')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow(False)
    window.show()
    sys.exit(app.exec_())
