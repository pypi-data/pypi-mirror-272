import time
from datetime import datetime
from datetime import timedelta


class SparrowDB(object):
    def __init__(self):
        self._data_key_value_ = {}
        self._data_body_ = {}

    def _is_key_value_overdue_(self, key: str):
        """
        检测key_value的值是否过期，过期就删除
        :param key: 值的key
        :return:
        """
        try:
            valid_time = self._data_key_value_.get(key).get("valid_time")
            if valid_time is not None:
                valid_time = float(valid_time)
                set_time = float(self._data_key_value_.get(key).get("set_time"))
                set_timestamp = datetime.fromtimestamp(set_time)
                valid_time = set_timestamp + timedelta(seconds=float(valid_time))
                valid_timestamp = time.mktime(valid_time.timetuple())
                new_time = time.time()
                if new_time > valid_timestamp:
                    del self._data_key_value_[key]
        except:
            pass

    def _is_body_overdue_(self, key: str):
        """
        检测body的值是否过期，过期就删除
        :param key: 值的key
        :return:
        """
        try:
            valid_time = self._data_body_.get(key).get("valid_time")
            if valid_time is not None:
                valid_time = float(valid_time)
                set_time = float(self._data_body_.get(key).get("set_time"))
                set_timestamp = datetime.fromtimestamp(set_time)
                valid_time = set_timestamp + timedelta(seconds=float(valid_time))
                valid_timestamp = time.mktime(valid_time.timetuple())
                new_time = time.time()
                if new_time > valid_timestamp:
                    del self._data_body_[key]
        except:
            pass

    def set_key_value(self, key: str, value: str, valid_time: float = None):
        """
        向key_value加入数据
        :param key: 键名
        :param value: 键值
        :param valid_time: 过期时间
        :return:
        """
        self._is_key_value_overdue_(key)
        if key in self._data_key_value_.keys():
            return f"{key} already in SparrowDB"
        else:
            self._data_key_value_[key] = {"value": value, "valid_time": valid_time, "set_time": time.time()}
            return self._data_key_value_[key]

    def reset_key_value(self, key: str, value: str, valid_time: float = None):
        """
        重新设置key_value的某个数据的值
        :param key: 键名
        :param value: 键值
        :param valid_time: 过期时间
        :return:
        """
        self._is_key_value_overdue_(key)
        if key in self._data_key_value_.keys():
            self._data_key_value_[key] = {"value": value, "valid_time": valid_time, "set_time": time.time()}
            return self._data_key_value_[key]
        else:
            return f"{key} not found in SparrowDB"

    def get_key_value(self, key: str):
        """
        获取key_value中某个数据的值
        :param key: 键名
        :return:
        """
        self._is_key_value_overdue_(key)
        if key in self._data_key_value_.keys():
            return {key: self._data_key_value_[key]['value']}
        else:
            return f"{key} not found in SparrowDB"

    def delete_key_value(self, key: str):
        """
        删除key_value中某个数据
        :param key: 键名
        :return:
        """
        self._is_key_value_overdue_(key)
        if key in self._data_key_value_.keys():
            data = {"key": key, "value": self._data_key_value_[key]['value']}
            del self._data_key_value_[key]
            return data
        else:
            return f"{key} not found  in SparrowDB"

    def set_body(self, key: str, body: dict, valid_time: float = None):
        """
        行body中加入数据
        :param key: 键名
        :param body: 键值
        :param valid_time: 过期时间
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():

            return f"{key} already in SparrowDB"
        else:
            self._data_body_[key] = {"value": body, "valid_time": valid_time, "set_time": time.time()}
            return self._data_body_[key]

    def reset_body(self, key: str, body: dict, valid_time: float = None):
        """
        重新设置body中的某个数据
        :param key: 键名
        :param body: 键值
        :param valid_time: 过期时间
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():
            body_key = body.get("key")
            body_value = body.get("value")
            self._data_body_[key]["value"][body_key] = body_value
            self._data_body_[key]["valid_time"] = valid_time
            self._data_body_[key]["set_time"] = time.time()
            return self._data_body_[key]
        else:
            return f"{key} not found in SparrowDB"

    def reset_body_all(self, key: str, body: dict, valid_time: float = None):
        """
        重新设置body中的某个数据
        :param key: 键名
        :param body: 键值
        :param valid_time: 过期时间
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():
            self._data_body_[key]["value"] = body
            self._data_body_[key]["valid_time"] = valid_time
            self._data_body_[key]["set_time"] = time.time()
            return self._data_body_[key]
        else:
            return f"{key} not found in SparrowDB"

    def get_body(self, key: str):
        """
        获取body中的某个值
        :param key: 键名
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():
            return {key: self._data_body_[key]['value']}
        else:
            return f"{key} not found in SparrowDB"

    def delete_body(self, key: str):
        """
        删除body中的某个值
        :param key: 键名
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():
            data = {"key": key, "value": self._data_body_[key]['value']}
            del self._data_body_[key]
            return data
        else:
            return f"{key} not found  in SparrowDB"

    def set_key_value_valid_time(self, key: str, valid_time: float):
        """
        重新设置key_value中某个值的过期时间
        :param key: 键名
        :param valid_time: 过期时间
        :return:
        """
        self._is_key_value_overdue_(key)
        if key in self._data_key_value_.keys():
            self._data_key_value_[key]["valid_time"] = valid_time
            self._data_key_value_[key]["set_time"] = time.time()
            return self._data_key_value_[key]
        else:
            return f"{key} not found in SparrowDB"

    def set_body_valid_time(self, key: str, valid_time: float):
        """
        重新设置body中某个值的过期时间
        :param key: 键名
        :param valid_time: 过期时间
        :return:
        """
        self._is_body_overdue_(key)
        if key in self._data_body_.keys():
            self._data_body_[key]["valid_time"] = valid_time
            self._data_body_[key]["set_time"] = time.time()
            return self._data_body_[key]
        else:
            return f"{key} not found in SparrowDB"

    def get_all_body(self):
        """
        获取body的所有值
        :return:
        """
        for key in self._data_body_.keys():
            self._is_body_overdue_(key)
        return self._data_body_

    def get_all_by_key(self):
        """
        获取key_value的所有值
        :return:
        """
        for key in self._data_key_value_.keys():
            self._is_key_value_overdue_(key)
        return self._data_key_value_
