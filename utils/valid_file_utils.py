from pathlib import Path
import re


class ValidFileUtils(object):
    @classmethod
    def check_dir_is_already(cls, check_path: str):
        """
        检查某个目录是否存在
        :return:
        """
        path = Path(check_path)
        if not path.exists():
            return False, f'{check_path}不存在'
        elif path.is_file():
            return False, f'{check_path}不是目录'
        return True, ''

    @classmethod
    def check_path_is_already(cls, check_path):
        """
        检查某个路径是否存在
        :param check_path:
        :return:
        """
        path = Path(check_path)
        if not path.exists():
            return False, f'{check_path}不存在，请检查'
        return True, ''

    @classmethod
    def check_time_edit(cls, str1):
        pattern = r"(^\d+(\*\d)*\d$)"
        compile = re.compile(pattern)
        res = compile.match(str1)
        return res
