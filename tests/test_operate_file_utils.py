import unittest
import os
from utils.operate_file_utils import OperateFileUtils


class TestOperateFileUtils(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_check_cp_file_not_source_path(self):
        try:
            res, msg = OperateFileUtils.cp_file('no_exists', '', '')
        except RuntimeError as e:
            self.assertEqual(str(e), 'no_exists不存在，请检查')

    def test_check_cp_file_no_target_path(self):
        try:
            res, msg = OperateFileUtils.cp_file('', 'no_exists', '')
        except RuntimeError as e:
            self.assertEqual(str(e), 'no_exists不存在')

    def test_check_cp_file_success(self):
        res, msg = OperateFileUtils.cp_file('./test_source_a/a', './test_target_b', './test_source_a')
        self.assertTrue(os.path.exists('test_target_b/a'))

    def test_check_cp_file_file_success(self):
        res, msg = OperateFileUtils.cp_file('./test_source_a/1', './test_target_b', './test_source_a')
        self.assertTrue(os.path.exists('test_target_b/1'))
        self.assertTrue(os.path.isfile('test_target_b/1'))


if __name__ == '__main__':
    unittest.main()
