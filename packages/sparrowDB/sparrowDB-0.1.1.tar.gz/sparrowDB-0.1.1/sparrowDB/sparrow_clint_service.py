"""
sparrowDB 服务器端
"""
import json
from sparrowApi import SparrowApi
from sparrowApi import ContentType
from sparrowDB.sparrow import SparrowDB
from sparrowDB.config import *
from sparrowDB.tools import SparrowValidTimeError

app = SparrowApi(__name__)
sparrow = SparrowDB()

password = input("Enter your password: ")
username = input("Enter your username: ")


class SparrowDBService(object):
    @staticmethod
    @app.post("/", content_type=ContentType.JSON)
    def main(data, headers):
        """
        :param data: SparrowApi向函数注入获取的数据
        :param headers: SparrowApi向函数注入获取的请求头
        :return:
        """
        if headers.get("SparrowApi"):
            if headers.get("Password") == password and headers.get("Username") == username:
                command = data.get("command").replace("+", " ")
                command_list = command.split(" ")
                if command_list[0] == "set":
                    if len(command_list) == 3:
                        result = sparrow.set_key_value(command_list[1], command_list[2])
                        return json.dumps({"status": "ok", "data": result})
                    elif len(command_list) == 4:
                        try:
                            valid_time = float(command_list[3])
                            result = sparrow.set_key_value(command_list[1], command_list[2], valid_time)
                            return json.dumps({"status": "ok", "data": result})
                        except Exception as e:
                            print(e)
                            return json.dumps(
                                {"status": "bad", "data": f"{command} -> {command_list[3]} is Invalid time"})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "get":
                    if len(command_list) == 2:
                        result = sparrow.get_key_value(command_list[1])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "reset":
                    if len(command_list) == 3:
                        result = sparrow.reset_key_value(command_list[1], command_list[2])
                        return json.dumps({"status": "ok", "data": result})
                    elif len(command_list) == 4:
                        try:
                            valid_time = float(command_list[3])
                            result = sparrow.reset_key_value(command_list[1], command_list[2], valid_time)
                            return json.dumps({"status": "ok", "data": result})
                        except SparrowValidTimeError:
                            return json.dumps(
                                {"status": "bad", "data": f"{command} -> {command_list[3]} is Invalid time"})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "delete":
                    if len(command_list) == 2:
                        result = sparrow.delete_key_value(command_list[1])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "set_body":
                    body = [i for i in command_list[2].replace("%2C", ",").split(",")]
                    insert_dict = {}
                    for insert_body in body:
                        insert_dict[insert_body.replace("%3D", "=").split("=")[0]] = \
                            insert_body.replace("%3D", "=").split("=")[1]
                    if len(command_list) == 3:
                        result = sparrow.set_body(command_list[1], insert_dict)
                        return json.dumps({"status": "ok", "data": result})
                    elif len(command_list) == 4:
                        try:
                            valid_time = float(command_list[3])
                            result = sparrow.set_body(command_list[1], insert_dict, valid_time)
                            return json.dumps({"status": "ok", "data": result})
                        except SparrowValidTimeError:
                            return json.dumps(
                                {"status": "bad", "data": f"{command} -> {command_list[3]} is Invalid time"})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "reset_body_all":
                    body = [i for i in command_list[2].replace("%2C", ",").split(",")]
                    insert_dict = {}
                    for insert_body in body:
                        insert_dict[insert_body.replace("%3D", "=").split("=")[0]] = \
                            insert_body.replace("%3D", "=").split("=")[1]
                    if len(command_list) == 3:
                        result = sparrow.reset_body_all(command_list[1], insert_dict)
                        return json.dumps({"status": "ok", "data": result})
                    elif len(command_list) == 4:
                        try:
                            valid_time = float(command_list[3])
                            result = sparrow.reset_body_all(command_list[1], insert_dict, valid_time)
                            return json.dumps({"status": "ok", "data": result})
                        except SparrowValidTimeError:
                            return json.dumps(
                                {"status": "bad", "data": f"{command} -> {command_list[3]} is Invalid time"})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "reset_body":
                    print(command_list)
                    insert_dict = {"key": command_list[2].replace("%3D", "=").split("=")[0],
                                   "value": command_list[2].replace("%3D", "=").split("=")[1]}
                    if len(command_list) == 3:
                        result = sparrow.reset_body(command_list[1], insert_dict)
                        return json.dumps({"status": "ok", "data": result})
                    elif len(command_list) == 4:
                        try:
                            valid_time = float(command_list[3])
                            result = sparrow.reset_body(command_list[1], insert_dict, valid_time)
                            return json.dumps({"status": "ok", "data": result})
                        except SparrowValidTimeError:
                            return json.dumps(
                                {"status": "bad", "data": f"{command} -> {command_list[3]} is Invalid time"})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "get_body":
                    if len(command_list) == 2:
                        result = sparrow.get_body(command_list[1])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "delete_body":
                    if len(command_list) == 2:
                        result = sparrow.delete_body(command_list[1])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "set_body_time":
                    if len(command_list) == 3:
                        result = sparrow.set_body_valid_time(command_list[1], command_list[2])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "set_time":
                    if len(command_list) == 3:
                        result = sparrow.set_key_value_valid_time(command_list[1], command_list[2])
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "get_all_body":
                    if len(command_list) == 1:
                        result = sparrow.get_all_body()
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "get_all":
                    if len(command_list) == 1:
                        result = sparrow.get_all_by_key()
                        return json.dumps({"status": "ok", "data": result})
                    else:
                        return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
                elif command_list[0] == "test":
                    return json.dumps({"status": "ok", "data": "connect is successful"})
                else:
                    return json.dumps({"status": "bad", "data": f"{command} is Invalid command"})
            else:
                return json.dumps({"status": "bad", "data": "Password or Username is required"})
        else:
            return json.dumps({"status": "bad", "data": "headers is not required"})

    @staticmethod
    def run(host: str = None, port: int = None, try_model: bool = None, show_error: bool = None, log_file: str = None, default_listen: int = None, is_save_log: bool = None):
        """
        :param host: 启动ip，不输入默认从config文件中读取，默认127.0.0.1
        :param port: 启动端口，不输入默认从config文件中读取，默认712
        :param try_model: try模式，不输入默认从config文件中读取，默认True
        :param show_error: 显示错误信息，不输入默认从config文件中读取，默认True
        :param log_file: 日志记录文件，不输入默认从config文件中读取，默认sparrow.log
        :param default_listen: 监听数量，不输入默认从config文件中读取，默认1
        :param is_save_log: 是否保存日志，不输入默认从config文件中读取，默认False
        :return:
        """
        if host is None:
            host = HOST
        if port is None:
            port = PORT
        if try_model is None:
            try_model = TRY_MODEL
        if show_error is None:
            show_error = SHOW_ERROR
        if log_file is None:
            log_file = LOG_FILE
        if default_listen is None:
            default_listen = DEFAULT_LISTEN
        if is_save_log is None:
            is_save_log = IS_SAVE_LOG
        app.run(host=host, port=port, try_model=try_model, show_error=show_error, log_file=log_file,
                default_listen=default_listen, is_save_log=is_save_log)


if __name__ == "__main__":
    run = SparrowDBService()
    run.run()
