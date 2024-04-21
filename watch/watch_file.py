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


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 记录新增文件及其位置
        print('新增了文件', event)

        if not event.is_directory:
            with open(log_file, "a") as f:
                f.write(f"Added: {event.src_path}\n")

    def on_modified(self, event):
        pass
        # print(event)
        # if not event.is_directory:
        # 记录修改文件及其位置
        # print(event.__dict__)
        # with open(log_file, "a") as f:
        #     f.write(f"Modified: {event.src_path}\n")

    def on_moved(self, event):
        print('moved', event.__dict__)

    def on_deleted(self, event):
        if not event.is_directory:
            # 记录删除文件及其位置
            with open(log_file, "a") as f:
                f.write(f"Deleted: {event.src_path}\n")


if __name__ == "__main__":
    file_path = 'test_path'
    WatchFiles.main(file_path, MyHandler())
