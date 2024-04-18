from utils.valid_file_utils import ValidFileUtils
from pathlib import Path
import shutil
import os


class OperateFileUtils(object):
    __doc__ = """
    操作文件
    """

    def create_dir(self):
        """
        创建目录
        :return:
        """

    @classmethod
    def cp_file(cls, source_path, target_path, source_base_path):
        """
        复制文件
        :param source_path:
        :param target_path:
        :param source_base_path
        :return:
        """
        res, msg = ValidFileUtils.check_path_is_already(source_path)
        if not res:
            raise RuntimeError(msg)
        res, msg = ValidFileUtils.check_dir_is_already(target_path)
        if not res:
            raise RuntimeError(msg)
        # 源路径和目标地址的 相对路径
        source_absolute_path = Path(source_base_path).absolute()
        target_absolute_path = Path(target_path).absolute()

        target_dir_path = ''  # 文件在备份盘拷贝的路径

        is_file = False

        source_dir_path = os.path.relpath(source_path, source_base_path)  # 源文件 在之前目录的相对位置
        full_target_path = target_absolute_path.joinpath(source_dir_path)
        # 检查源文件是否是文件
        if os.path.isfile(source_path):
            """
            1. 取到绝对位置
            2. 取到该文件所在的目录，
            3. 查看该文件要放在目标文件那个位置
            """
            path = Path(source_path)
            file_source_dir = path.parent.absolute()  # 文件所在目录
            target_dir_path = os.path.relpath(file_source_dir, source_absolute_path)
            full_target_path = target_absolute_path.joinpath(target_dir_path)
            is_file = True
        os.makedirs(full_target_path, exist_ok=True)

        if is_file:
            shutil.copy2(source_path, full_target_path)
        return True, full_target_path
