import time

from PyQt5.QtCore import pyqtSignal, QThread


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, watch_obj, source_file, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watch_obj = watch_obj
        self.source_file = source_file
        self.handler = handler

    def run(self):
        # while True:
        #     time.sleep(1)
        #     print('hello world')
        self.watch_obj.main(self.source_file, self.handler)

    def stop(self):
        # self.watch_obj.stop()
        # self.quit()
        if self.isRunning():
            self.terminate()
            self.watch_obj.stop()
