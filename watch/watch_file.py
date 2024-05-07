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
    sleet_time = 1

    @classmethod
    def stop(cls):
        """
        停止当前文件监听
        因为每个线程对象只能调用一下start所以这里在把哈上一次的终止完成之后从新创建一个observer对象
        :return:
        """
        if cls.observer.is_alive():
            # cls.is_stop = True
            cls.observer.stop()
            cls.observer.join(1)
            # https://python-watchdog.readthedocs.io/en/stable/api.html#module-watchdog.observers
            cls.observer = Observer()
            # cls.is_stop = True
            # cls.observer.stop()

    @classmethod
    def main(cls, file_path, handler):
        if not isinstance(handler, FileSystemEventHandler):
            raise ValueError('handler 必须是FileSystemEventHandler类')

        # 创建 Observer 对象并启动监视
        cls.observer.schedule(handler, path=file_path, recursive=True)
        cls.observer.start()

        try:
            # i = 0
            while cls.observer.is_alive():
                print(cls.sleet_time)
                print(111)
                time.sleep(cls.sleet_time)
            cls.observer.join(1)
        finally:
            cls.observer.stop()
            cls.observer.join()
