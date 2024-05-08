"""
sparrowDB 客服端
"""
import sys
import requests
from colorama import Fore
from colorama import init


class SparrowClint(object):
    def __init__(self):
        self.url = "http://127.0.0.1:712"
        self.headers = {"SparrowApi": "SparrowApi", "Password": "", "Username": ""}
        init(autoreset=True)

    def send_command(self, command: str):
        """
        发送命令
        :param command: 命令
        :return:
        """
        r = requests.post(self.url, data={"command": command}, headers=self.headers)
        return r.json()

    def main(self):
        """
        主方法
        :return:
        """
        while True:
            host = input("Enter Host:")
            if host == "":
                host = "127.0.0.1"
            port = input("Enter Port:")
            if port == "":
                port = "712"
            self.headers["Password"] = input("Enter Password:")
            self.headers["Username"] = input("Enter Username:")
            self.url = "http://{}:{}".format(host, port)
            try:
                r = None
                try:
                    r = requests.post(self.url, data={"command": "test"}, headers=self.headers)
                    print(f"->{r.json().get('status')}")
                    print(f"->{r.json().get('data')}")
                    if r.json().get('status') == "ok":
                        open_ = True
                    else:
                        status = input("Do you want to continue?(y or n)")
                        if status == "y":
                            continue
                        else:
                            break
                except:
                    open_ = False
                if open_:
                    if r.status_code == 200:
                        go = True
                        while go:
                            command = input("->")
                            if command == "exit":
                                sys.exit(0)
                            else:
                                result = self.send_command(command)
                                if result.get("status") == "ok":
                                    print(f"->{result.get('status')}")
                                    print(f"->{result.get('data')}")
                                else:
                                    print("->" + Fore.RED + f"{result.get('status')}")
                                    print("->" + Fore.RED + f"{result.get('data')}")
                    else:
                        print(f"{self.url} not sparrow service")
                else:
                    print(f"{self.url} connection error")
            except ConnectionError:
                print(f"{self.url}")


if __name__ == "__main__":
    sparrow_clint = SparrowClint()
    sparrow_clint.main()
