class SettingsUtils(object):
    """
    settings工具类
    """

    @classmethod
    def transfer_dict_to_list(cls, transfer_dict: dict):
        """
        转换字典为list
        :param transfer_dict:
        :return:
        """
        result = []
        if not isinstance(transfer_dict, dict):
            raise TypeError('transfer的类型必须是dict类型')
        for key, value in transfer_dict.items():
            result.append([key, value])
        return result
