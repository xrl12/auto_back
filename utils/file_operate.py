from watchdog.events import FileSystemEventHandler
from signal import Signals
import os
from utils.valid_file_utils import ValidFileUtils


class FileOperate(FileSystemEventHandler):
    def __init__(self, backup_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        res, msg = ValidFileUtils.check_dir_is_already(backup_path)
        if not res:
            raise RuntimeError(msg)
        else:
            self.backup_path = backup_path

    def on_created(self, event):
        """
        在监听文件新增的后
        :param event:
        :return:
        """
        print('新增了文件', event.__dict__)
        src_path = event.src_path


    def on_modified(self, event):
        print(event.__dict__, '修改了内容')
        if not event.is_directory:
            pass
            # 记录修改文件及其位置

            # with open(log_file, "a") as f:
            #     f.write(f"Modified: {event.src_path}\n")

    def on_deleted(self, event):
        print('删除了文件', event.__dict__)
        if not event.is_directory:
            pass
            # 记录删除文件及其位置
            # with open(log_file, "a") as f:
            #     f.write(f"Deleted: {event.src_path}\n")
