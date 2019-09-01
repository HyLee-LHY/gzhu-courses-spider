import http.cookiejar as HC

import requests


# 广大主页
class GzhuHome:
    def __init__(self):
        self.session = None

    def load_cookies(self, file_path="cookies.hylee"):
        self.session = requests.session()
        self.session.cookies = HC.LWPCookieJar(filename=file_path)
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("cookie文件不存在")

    # 获取登录参数
    def get_login_param(self, html, key, special=False):
        flag = None
        if special is False:
            flag = '"' + key + '" value="'
        else:
            flag = '"' + key + '" accesskey="l" value="'
        start = html.find(flag)
        if start != -1:
            start += len(flag)
        temp_string = html[start:]
        end = temp_string.find('"')
        if end != -1:
            result = temp_string[:end]
            return result
        return None

    def get_session(self, file="cookies.hylee"):  # 获取当前会话，通过session可自动管理cookie
        if self.session is None:
            self.session = requests.Session()
            self.session.cookies = HC.LWPCookieJar(filename=file)
            headers = {
                # "Content-Type": "application/x-www-form-urlencoded",  # post请求默认类型，可以不加
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
            self.session.headers.update(headers)
        return self.session

    # 登录广大主页
    def login(self, username, password):
        session = self.get_session()
        login_url = 'https://cas.gzhu.edu.cn/cas_server/login'
        response = session.get(login_url)
        login_page = response.text
        # login_page = response.read().decode("utf-8")  # 获取登录页面的源码
        captcha = self.get_login_param(login_page, 'captcha')
        warn = self.get_login_param(login_page, 'warn')
        lt = self.get_login_param(login_page, 'lt')
        execution = self.get_login_param(login_page, 'execution')
        _eventId = self.get_login_param(login_page, '_eventId')
        submit = self.get_login_param(login_page, 'submit', True)
        login_params = {"username": username, "password": password, "captcha": captcha, "warn": warn,
                        "lt": lt, "execution": execution, "_eventId": _eventId, "submit": submit}
        r = session.post(login_url, data=login_params)
        # print(r.text)
        if r.text.find("主页") != -1:
            print("登录广大主页成功")
            return True
        else:
            print("登录广大主页失败")
            return False
