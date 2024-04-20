from pathlib import Path
import unittest
from utils.valid_file_utils import ValidFileUtils


class TestValidFileUtils(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_check_dir_is_already_params_is_error(self):
        res = ValidFileUtils.check_dir_is_already('error_path')
        self.assertFalse(res[0])

    def test_check_dir_is_already_params_is_right(self):
        path = Path('')
        current_dir = path.cwd()
        res = ValidFileUtils.check_dir_is_already(current_dir)
        self.assertTrue(res[0])

    def test_check_dir_is_already_params_is_file(self):
        res = ValidFileUtils.check_dir_is_already(__file__)
        self.assertFalse(res[0])

    def test_check_path_is_already_params_is_right(self):
        path = Path('')
        current_dir = path.cwd()
        res = ValidFileUtils.check_path_is_already(current_dir)
        self.assertTrue(res[0])

    def test_check_path_is_already_is_error(self):
        res = ValidFileUtils.check_dir_is_already('error_path')
        self.assertFalse(res[0])


if __name__ == '__main__':
    unittest.main()
