import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 存储文件变化的日志文件
log_file = "../changes.log"


class WatchFiles(object):
    """
    监听文件类
    """
    observer = Observer()

    @classmethod
    def stop(cls):
        """
        停止当前文件监听
        :return:
        """
        if cls.observer.is_alive():
            cls.observer.stop()
            cls.observer.join()

    @classmethod
    def main(cls, file_path, handler):
        if not isinstance(handler, FileSystemEventHandler):
            raise ValueError('handler 必须是FileSystemEventHandler类')

        # 创建 Observer 对象并启动监视
        # observer = Observer()
        cls.observer.schedule(handler, path=file_path, recursive=True)
        cls.observer.start()
        try:
            i = 0
            while cls.observer.is_alive():
                cls.observer.join(1)
        finally:
            cls.observer.stop()
            cls.observer.join()
