from watchdog.events import FileSystemEventHandler

log_file = "changes.log"


class FileOperate(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            # 记录新增文件及其位置
            with open(log_file, "a") as f:
                f.write(f"Added: {event.src_path}\n")

    def on_modified(self, event):
        if not event.is_directory:
            # 记录修改文件及其位置
            print(event.__dict__)
            with open(log_file, "a") as f:
                f.write(f"Modified: {event.src_path}\n")

    def on_deleted(self, event):
        if not event.is_directory:
            # 记录删除文件及其位置
            with open(log_file, "a") as f:
                f.write(f"Deleted: {event.src_path}\n")
