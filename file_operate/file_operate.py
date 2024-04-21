import os
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from utils.valid_file_utils import ValidFileUtils
from utils.operate_file_utils import OperateFileUtils


class FileOperate(FileSystemEventHandler):
    def __init__(self, backup_path, source_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        res, msg = ValidFileUtils.check_dir_is_already(backup_path)
        if not res:
            raise RuntimeError(msg)
        res, msg = ValidFileUtils.check_dir_is_already(source_path)
        if not res:
            raise RuntimeError(msg)

        self.backup_path = backup_path
        self.source_path = source_path

    def on_created(self, event):
        """
        在监听文件新增的后
        :param event:
        :return:
        """
        src_path = event.src_path
        OperateFileUtils.cp_file(src_path, self.backup_path, self.source_path)

    def on_modified(self, event):
        src_path = event.src_path
        OperateFileUtils.cp_file(src_path, self.backup_path, self.source_path)

    def on_deleted(self, event):
        src_path = event.src_path
        OperateFileUtils.del_file(src_path, self.backup_path, self.source_path)
        # 记录删除文件及其位置
        # with open(log_file, "a") as f:
        #     f.write(f"Deleted: {event.src_path}\n")

    def on_moved(self, event: FileSystemEvent):
        print('event', event.__dict__)
        OperateFileUtils.moved_file(event.src_path, event.dest_path, self.source_path, self.backup_path, )
