from qt.window import MyWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow(False)
    window.show()
    sys.exit(app.exec_())
