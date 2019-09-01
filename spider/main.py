# encoding:utf-8
from spider.education_system import EducationSystem
from spider.login_gzhu_home import GzhuHome

if __name__ == '__main__':
    gzhu_login = GzhuHome()
    while True:
        x = input("请选择操作:\n1.账号密码登录\n2.cookie登录\n#.退出\n").strip()  # 获取用户输入并去除空格
        if x == '1':  # 账号密码登录
            username = input("请输入账号:\n")
            password = input("请输入密码:\n")
            success = gzhu_login.login(username, password)
            if success is True:
                s = gzhu_login.get_session()
                education_system = EducationSystem(s)
        elif x == "2":
            x = input("请输入cookie文件的路径(直接回车默认:cookies.hylee):\n").strip()
            if x == "":  # 直接回车
                gzhu_login.load_cookies()
            else:
                gzhu_login.load_cookies(file_path=x)
            education_system = EducationSystem(gzhu_login.get_session())
        elif x == '#':
            break
        else:
            print("输入有误，请重新输入")
