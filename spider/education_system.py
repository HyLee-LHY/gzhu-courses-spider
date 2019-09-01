import json


# 教务系统 发送网络请求时参数可多不可少(有时候少了好像也不会出现错误)
class EducationSystem:
    def __init__(self, session):
        self.session = session
        self.modules = None
        self.public_params = None
        self.selectable_causes = None
        self.html = None
        self.cause_type = None
        r = self.session.get("http://jwxt.gzhu.edu.cn/sso/lyiotlogin")  # 登录教务系统
        if r.text.find("广州大学教学综合信息服务平台") != -1:
            print("登录教务系统成功")
            self.session.cookies.save(ignore_discard=True, ignore_expires=True)
            self.get_cause_types()
        else:
            print("登录教务系统失败")

    # 获取课程类型
    def get_cause_types(self):
        while True:
            x = input("获取课程类型(体育、主修、选修)途径:\n1.教务系统\n2.本地文件\n#.退出\n").strip()
            if x == "1":
                self.init_modules_and_params()
                if len(self.modules) > 0:  # 获取到课程类型
                    self.select_cause_type()
                else:  # 没有获取到课程类型
                    print("没有课程类型可选")
            elif x == "2":
                x = input("请输入文件路径(直接回车默认:modules.hylee):\n").strip()
                if x == "":
                    self.init_modules_and_params(module_from_file=True)
                else:
                    self.init_modules_and_params(module_from_file=True, module_file_path=x)
                if len(self.modules) > 0:  # 获取到课程类型
                    self.select_cause_type()
                else:  # 没有获取到课程类型
                    print("没有课程类型可选")
            elif x == "#":
                break
            else:
                print("输入有误")

    # 选择课程类型
    def select_cause_type(self):
        while True:
            x = input("请选择课程类型(输入数字即可,#号退出):\n").strip()
            if x == "#":
                break
            try:
                x = int(x)
                if (x < 1) or (x > len(self.modules)):
                    print("输入有误")
                else:
                    self.cause_type = x - 1
                    self.show_cause_options()
                    break
            except:
                print("输入有误")

    # 显示课程选项
    def show_cause_options(self):
        while True:
            x = input("请选择操作:\n1.选课\n2.退课\n3.已选课程\n#.退出\n").strip()
            if x == "1":
                self.subscribe()
            elif x == "2":
                self.withdraw()
            elif x == "3":
                self.show_selected_cause()
            elif x == "#":
                break
            else:
                print("输入有误")

    # 显示已选课程
    def show_selected_cause(self):
        while True:
            x = input("请选择操作:\n1.从教务系统获取已选课程\n2.从本地加载已选课程\n#.退出\n").strip()
            if x == "1":
                self.get_selected_causes()
            elif x == "2":
                x = input("请输入已选课程文件路径(直接回车默认:kc_selected.hylee):\n").strip()
                if x == "":  # 直接回车
                    self.load_selected_cause()
                else:
                    self.load_selected_cause(file_path=x)
            elif x == "#":
                break
            else:
                print("输入有误")

    # 获取返回的html中存在的参数 参数一般都有相同的特征
    def get_selectable_causes_param(self, html, key):
        flag = 'id="' + key + '" value="'
        start = html.find(flag)
        if start != -1:
            start += len(flag)
        temp_string = html[start:]
        end = temp_string.find('"')
        if end != -1:
            result = temp_string[:end]
            return result
        return None

    # 获取粗略信息需要的参数
    def get_rough_params(self, html):
        rwlx = self.get_selectable_causes_param(html, "rwlx")
        xkly = self.get_selectable_causes_param(html, "xkly")
        bklx_id = self.get_selectable_causes_param(html, "bklx_id")
        sfkknj = self.get_selectable_causes_param(html, "sfkknj")
        sfkkzy = self.get_selectable_causes_param(html, "sfkkzy")
        sfznkx = self.get_selectable_causes_param(html, "sfznkx")
        zdkxms = self.get_selectable_causes_param(html, "zdkxms")
        sfkxq = self.get_selectable_causes_param(html, "sfkxq")
        sfkcfx = self.get_selectable_causes_param(html, "sfkcfx")
        kkbk = self.get_selectable_causes_param(html, "kkbk")
        kkbkdj = self.get_selectable_causes_param(html, "kkbkdj")
        sfkgbcx = self.get_selectable_causes_param(html, "sfkgbcx")
        sfrxtgkcxd = self.get_selectable_causes_param(html, "sfrxtgkcxd")
        tykczgxdcs = self.get_selectable_causes_param(html, "tykczgxdcs")
        rlkz = self.get_selectable_causes_param(html, "rlkz")

        params = {"rwlx": rwlx, "xkly": xkly, "bklx_id": bklx_id, "sfkknj": sfkknj, "sfkkzy": sfkkzy,
                  "sfznkx": sfznkx, "zdkxms": zdkxms, "sfkxq": sfkxq, "sfkcfx": sfkcfx, "kkbk": kkbk, "kkbkdj": kkbkdj,
                  "sfkgbcx": sfkgbcx, "sfrxtgkcxd": sfrxtgkcxd, "tykczgxdcs": tykczgxdcs, "rlkz": rlkz}
        return params

    # 获取点击选课按钮的参数，html页面的数据都有一定规律，故可以按照相同的方法获得参数值
    def get_selectable_causes_params(self, html, url, start=1, end=10):
        xqh_ids = self.get_selectable_causes_param(html, "xqh_id")
        jg_id = self.get_selectable_causes_param(html, "jg_id_1")
        zyh_id = self.get_selectable_causes_param(html, "zyh_id")
        zyfx_id = self.get_selectable_causes_param(html, "zyfx_id")
        njdm_id = self.get_selectable_causes_param(html, "njdm_id")
        bh_id = self.get_selectable_causes_param(html, "bh_id")
        xbm = self.get_selectable_causes_param(html, "xbm")
        xslbdm = self.get_selectable_causes_param(html, "xslbdm")
        ccdm = self.get_selectable_causes_param(html, "ccdm")
        xsbj = self.get_selectable_causes_param(html, "xsbj")
        xkxnm = self.get_selectable_causes_param(html, "xkxnm")
        xkxqm = self.get_selectable_causes_param(html, "xkxqm")
        kklxdm = self.get_selectable_causes_param(html, "firstKklxdm")
        jxbzb = self.get_selectable_causes_param(html, "jxbzb")
        params = {"xqh_ids": xqh_ids, "jg_id": jg_id, "zyh_id": zyh_id, "zyfx_id": zyfx_id, "njdm_id": njdm_id,
                  "bh_id": bh_id, "xbm": xbm, "xslbdm": xslbdm, "ccdm": ccdm, "xsbj": xsbj, "xkxnm": xkxnm,
                  "xkxqm": xkxqm, "kklxdm": kklxdm, "jxbzb": jxbzb, "kspage": start, "jspage": end}
        print(url + "需要提交的参数为:")
        print(params)
        return params

    # 获取课程详细信息需要提交的参数，html页面的数据都有一定规律，故可以按照相同的方法获得参数值
    def get_public_params(self, html):
        # xqh_id jg_id zyh_id zyfx_id njdm_id bh_id xbm xslbdm ccdm xsbj xkxnm xkxqm kklxdm kch_id(通过另外的方式)
        xqh_id = self.get_selectable_causes_param(html, "xqh_id")
        jg_id = self.get_selectable_causes_param(html, "jg_id_1")
        zyh_id = self.get_selectable_causes_param(html, "zyh_id")
        zyfx_id = self.get_selectable_causes_param(html, "zyfx_id")
        njdm_id = self.get_selectable_causes_param(html, "njdm_id")
        bh_id = self.get_selectable_causes_param(html, "bh_id")
        xbm = self.get_selectable_causes_param(html, "xbm")
        xslbdm = self.get_selectable_causes_param(html, "xslbdm")
        ccdm = self.get_selectable_causes_param(html, "ccdm")
        xsbj = self.get_selectable_causes_param(html, "xsbj")
        xkxnm = self.get_selectable_causes_param(html, "xkxnm")
        xkxqm = self.get_selectable_causes_param(html, "xkxqm")
        kklxdm = self.get_selectable_causes_param(html, "firstKklxdm")
        params = {"xqh_id": xqh_id, "jg_id": jg_id, "zyh_id": zyh_id, "zyfx_id": zyfx_id, "njdm_id": njdm_id,
                  "bh_id": bh_id, "xbm": xbm, "xslbdm": xslbdm, "ccdm": ccdm, "xsbj": xsbj, "xkxnm": xkxnm,
                  "xkxqm": xkxqm, "kklxdm": kklxdm}
        return params

    # 从文件加载课程信息
    def load_local_causes(self, file_path="kc_0.hylee"):
        # print("课程名称 学分 教师信息 上课时间 课程性质 教学模式 选课备注 课程id 教学班id xxkbj")
        local_causes_info = []
        count = 1
        with open(file_path, 'r', encoding="utf-8") as file:  # 打开文件保存课程信息的文件
            for line in file:  # 读取文件内容
                local_causes_info = json.loads(line)  # 将文件内容解析为课程对象集合
            for item in local_causes_info:  # 遍历课程对象集合并打印
                print(str(count), item.get("kcmc"), item.get("xf"), item.get("jsxx"), item.get("sksj"),
                      item.get("kcxzmc"), item.get("jxms"), item.get("xkbz"), item.get("kch_id"),
                      item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                count = count + 1
        return local_causes_info

    # 获取详细信息所需要的参数
    def get_detail_params(self, html, file_path="modules.hylee"):
        rwlx = self.get_selectable_causes_param(html, "rwlx")
        self.modules[self.cause_type].append(rwlx)
        xkly = self.get_selectable_causes_param(html, "xkly")
        bklx_id = self.get_selectable_causes_param(html, "bklx_id")
        sfkknj = self.get_selectable_causes_param(html, "sfkknj")
        sfkkzy = self.get_selectable_causes_param(html, "sfkkzy")
        sfznkx = self.get_selectable_causes_param(html, "sfznkx")
        zdkxms = self.get_selectable_causes_param(html, "zdkxms")
        sfkxq = self.get_selectable_causes_param(html, "sfkxq")
        sfkcfx = self.get_selectable_causes_param(html, "sfkcfx")
        kkbk = self.get_selectable_causes_param(html, "kkbk")
        kkbkdj = self.get_selectable_causes_param(html, "kkbkdj")
        rlkz = self.get_selectable_causes_param(html, "rlkz")
        self.modules[self.cause_type].append(rlkz)
        rlzlkz = self.get_selectable_causes_param(html, "rlzlkz")
        self.modules[self.cause_type].append(rlzlkz)
        xklc = self.get_selectable_causes_param(html, "xklc")
        self.modules[self.cause_type].append(xklc)
        with open(file_path, 'w', encoding="utf-8") as file:  # 将数据写到文件中
            file.write(json.dumps(self.modules))
        params = {"rwlx": rwlx, "xkly": xkly, "bklx_id": bklx_id, "sfkknj": sfkknj,
                  "sfkkzy": sfkkzy, "sfznkx": sfznkx, "zdkxms": zdkxms, "sfkxq": sfkxq,
                  "sfkcfx": sfkcfx, "kkbk": kkbk, "kkbkdj": kkbkdj, "rlkz": rlkz}
        return params

    # 选课初始化参数和模块
    def init_modules_and_params(self, module_from_file=False, module_file_path="modules.hylee"):
        select_cause_url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default"  # 点击自主选课请求的url
        self.html = self.session.get(select_cause_url).text  # 获取自主选课html页面
        if module_from_file is True:  # 本地加载课程类型
            self.load_modules(module_file_path)
        else:
            self.modules = self.get_modules(self.html)  # 获取课程的类型 体育 选修 主修
        self.public_params = self.get_public_params(self.html)  # 自主选课页面有的参数,一般每次请求都要加上

    # 获取可选课程的方法
    def get_selectable_causes(self, start=1, end=10000000, file_path=None):
        # if self.public_params is None or self.modules is None:
        #     self.init_modules_and_params(module_from_file, module_file_path)
        # if len(self.modules) <= self.cause_type:
        #     print("输入cause_type大于可选课程类型数量")
        #     return
        xszxzt = self.get_selectable_causes_param(self.html, "xszxzt")
        kklxdm = self.modules[self.cause_type][0]
        params = {"xkkz_id": self.modules[self.cause_type][1], "xszxzt": xszxzt}
        res = self.session.post("http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbDisplay.html?gnmkdm=N253512",
                                data=params)  # 获取参数的网页
        # 获取粗略的课程信息
        rough_params = self.get_rough_params(res.text)
        rough_params = dict(self.public_params, **rough_params)
        rough_params["kklxdm"] = kklxdm
        rough_params["jxbzb"] = None
        rough_params["kspage"] = start
        rough_params["jspage"] = end
        r = self.session.post("http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512",
                              data=rough_params)
        data = json.loads(r.text).get("tmpList")
        # 获取详细的课程信息
        detail_params = self.get_detail_params(res.text)
        detail_params = dict(detail_params, **self.public_params)
        detail_params["kklxdm"] = kklxdm
        url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512"
        detail_causes_info = []
        count = 1
        for item in data:
            kch_id = item.get("kch_id")  # 课程id
            detail_params["kch_id"] = kch_id
            detail_params["cxbj"] = item.get("cxbj")
            detail_params["fxbj"] = item.get("fxbj")
            detail_item = json.loads(self.session.post(url, data=detail_params).text)
            for detail in detail_item:
                # 课程名称 学分 教师信息 上课时间 课程性质 教学模式 选课备注 课程id 教学班id xxkbj
                kcxq = {"kcmc": item.get("kcmc"), "xf": item.get("xf"), "jsxx": detail.get("jsxx"),
                        "sksj": detail.get("sksj"), "kcxzmc": detail.get("kcxzmc"),
                        "jxms": detail.get("jxms"), "xkbz": detail.get("xkbz"), "kch_id": kch_id,
                        "jxb_id": item.get("jxb_id"), "xxkbj": item.get("xxkbj"), "cxbj": item.get("cxbj")}  # 课程详情
                detail_causes_info.append(kcxq)
                print(str(count), item.get("kcmc"), item.get("xf"), detail.get("jsxx"),
                      detail.get("sksj"), detail.get("kcxzmc"),
                      detail.get("jxms"), detail.get("xkbz"), kch_id,
                      item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                count += 1
        print("数据大小为：", len(detail_causes_info))
        if file_path is None:
            file_path = "kc_" + str(self.cause_type) + ".hylee"
        with open(file_path, 'w', encoding="utf-8") as file:  # 将数据写到文件中
            file.write(json.dumps(detail_causes_info))
        return detail_causes_info

    def load_modules(self, file_path="modules.hylee"):
        with open(file_path, 'r', encoding="utf-8") as file:  # 打开文件保存课程信息的文件
            for line in file:  # 读取文件内容
                self.modules = json.loads(line)
                count = 1
                for item in self.modules:
                    print("课程类型" + str(count), item)
                    count += 1

    # 获取课程类型（体育、主修、选修）
    # queryCourse(this,'01','90BF46F4F75374F8E053206411AC28F7')
    # 获取 01 90BF46F4F75374F8E053206411AC28F7两个重要字符串
    def get_modules(self, html, file_path="modules.hylee"):
        result = []
        key = "queryCourse("
        start = html.find(key)
        if start != -1:
            start += len(key)
        end = html.find(")", start)
        while (start != -1) and (end != -1):
            s = html[start:end].split(",")  # 根据逗号分割字符串
            result.append([s[1].replace("'", ""), s[2].replace("'", "")])  # 去除单引号
            if end == -1:
                break
            start = html.find(key, end)
            if start == -1:
                break
            start += len(key)
            end = html.find(")", start)
        if len(result) != 0:
            with open(file_path, 'w', encoding="utf-8") as file:  # 将数据写到文件中
                file.write(json.dumps(result))
        count = 1
        for item in result:
            print("课程类型" + str(count), item)
            count += 1
        return result  # 将结果返回

    # 获取选课所需要的参数
    def get_subscribe_cause_params(self, cause, url, file_path="subscribe_cause_params.hylee"):
        # rwlx rlkz rlzlkz xklc
        params = {"jxb_ids": cause.get("jxb_id"), "kch_id": cause.get("kch_id"),
                  "kcmc": cause.get("kcmc"), "rwlx": self.modules[self.cause_type][2],
                  "rlkz": self.modules[self.cause_type][3], "rlzlkz": self.modules[self.cause_type][4],
                  "sxbj": "1", "xxkbj": cause.get("xxkbj"), "qz": "0", "cxbj": cause.get("cxbj"),
                  "xkkz_id": self.modules[self.cause_type][1], "njdm_id": self.public_params.get("njdm_id"),
                  "zyh_id": self.public_params.get("zyh_id"), "kklxdm": self.modules[self.cause_type][0],
                  "xklc": self.modules[self.cause_type][5], "xkxnm": self.public_params.get("xkxnm"),
                  "xkxqm": self.public_params.get("xkxqm")}
        print(url + "需要提交的参数为:")
        print(params)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(params))
        return params

    # 选课的方法
    def subscribe(self):
        # if self.public_params is None:
        #     self.init_modules_and_params(module_from_file=module_from_file, module_file_path=module_file_path)
        username = input("请输入学号:\n")
        url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=" + username
        while True:
            x = input("请选择操作:\n1.从教务系统获取课程\n2.本地课程文件加载课程\n3.开始选课(请先通过1或者2获取课程信息)\n#.退出\n").strip()
            if x == "1":
                try:
                    start = int(input("请输入开始的位置:\n").strip())
                    end = int(input("请输入结束的位置:\n").strip())
                    file_path = input("请输入保存文件的路径(直接回车使用默认路径):\n").strip()
                    if file_path == "":  # 直接回车
                        self.selectable_causes = self.get_selectable_causes(start, end)
                    else:
                        self.selectable_causes = self.get_selectable_causes(start, end, file_path=file_path)
                except:
                    print("输入有误")
            elif x == "2":
                x = input("请输入本地课程文件所在路径(直接回车默认路径:kc_0.hylee):\n").strip()
                if x == "":  # 默认路径
                    self.selectable_causes = self.load_local_causes()
                else:
                    self.selectable_causes = self.load_local_causes(file_path=x)
            elif x == "3":
                if self.selectable_causes is None or len(self.selectable_causes) == 0:
                    print("没有课程数据")
                    break
                self.search_causes(url)
            elif x == "#":
                break
            else:
                print("请输入合法操作")

    # 搜索课程
    def search_causes(self, url):
        while True:
            x = input("请选择搜索类型:\n1.按教师搜索\n2.按照课程名称搜索\n#.退出\n").strip()
            if x == "1":
                self.search_by_teacher(url)
            elif x == "2":
                self.search_by_cause_name(url)
            elif x == "#":
                break
            else:
                print("输入有误")

    # 通过课程名称选课
    def search_by_cause_name(self, url):
        while True:
            x = input("请输入课程名称(输入#退出):\n").strip()
            if x == "#":
                break
            result = []
            for item in self.selectable_causes:
                if x in item.get("kcmc"):
                    result.append(item)
            count = 1
            for item in result:
                print(str(count), item.get("kcmc"), item.get("xf"), item.get("jsxx"), item.get("sksj"),
                      item.get("kcxzmc"), item.get("jxms"), item.get("xkbz"), item.get("kch_id"),
                      item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                count += 1
            if len(result) > 0:
                while True:
                    x = input("请选择课程(输入课程前面的数字即可,#号退出):\n")
                    try:
                        if x == "#":
                            break
                        x = int(x)
                        if (x < 1) or (x > len(result)):
                            print("输入有误")
                        else:
                            item = result[x - 1]
                            print("要选此课程?")
                            print(str(x), item.get("kcmc"), item.get("xf"), item.get("jsxx"), item.get("sksj"),
                                  item.get("kcxzmc"), item.get("jxms"), item.get("xkbz"), item.get("kch_id"),
                                  item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                            x = input("请选择操作:\n1.确定\n2.取消\n").strip()
                            if str(x) == "1":
                                params = self.get_subscribe_cause_params(item, url)
                                r = self.session.post(url, data=params)
                                if '{"flag":"1"}' in r.text:
                                    print("选课成功")
                                else:
                                    print(r.text)
                    except:
                        print("输入有误")
            else:
                print("没有找到该课程名称的课程")

    # 通过老师选课
    def search_by_teacher(self, url):
        while True:
            x = input("请输入教师名字(输入#退出):\n").strip()
            if x == "#":
                break
            result = []
            for item in self.selectable_causes:
                if x in item.get("jsxx"):
                    result.append(item)
            count = 1
            for item in result:
                print(str(count), item.get("kcmc"), item.get("xf"), item.get("jsxx"), item.get("sksj"),
                      item.get("kcxzmc"), item.get("jxms"), item.get("xkbz"), item.get("kch_id"),
                      item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                count += 1
            if len(result) > 0:
                while True:
                    x = input("请选择课程(输入课程前面的数字即可,#号退出):\n")
                    try:
                        if x == "#":
                            break
                        x = int(x)
                        if (x < 1) or (x > len(result)):
                            print("输入有误")
                        else:
                            item = result[x - 1]
                            print("要选此课程?")
                            print(str(x), item.get("kcmc"), item.get("xf"), item.get("jsxx"), item.get("sksj"),
                                  item.get("kcxzmc"), item.get("jxms"), item.get("xkbz"), item.get("kch_id"),
                                  item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                            x = input("请选择操作:\n1.确定\n2.取消\n").strip()
                            if str(x) == "1":
                                params = self.get_subscribe_cause_params(item, url)
                                r = self.session.post(url, data=params)
                                if '{"flag":"1"}' in r.text:
                                    print("选课成功")
                                else:
                                    print(r.text)
                    except:
                        print("输入有误")
            else:
                print("没有找到该老师的课程")

    # 获取退选课程的参数
    def get_withdraw_params(self, username, cause, url, file_path="withdraw_cause_params.hylee"):
        params = {"gnmkdm": "N253512", "su": username, "xkkz_id": self.modules[self.cause_type][1],
                  "jxb_id": cause.get("jxb_id"), "kch_id": cause.get("kch_id"), "xnm": self.public_params.get("xkxnm"),
                  "xqm": self.public_params.get("xkxqm")}
        print(url + "需要提交的参数为:")
        print(params)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(params))
        return params

    # 取消选课
    def withdraw(self):
        # if self.public_params is None:
        #     self.init_modules_and_params(module_from_file=module_from_file, module_file_path=module_file_path)
        username = input("请输入学号:\n")
        url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_xkJcInXksjZzxkYzb.html?gnmkdm=N253512&su="
        selected_causes = None
        while True:
            x = input("请选择操作:\n1.访问教务系统获取已选课程\n2.通过本地文件导入\n3.进行课程退选\n#.退出\n").strip()
            if x == "1":
                selected_causes = self.get_selected_causes()
            elif x == "2":
                x = input("请输入已选课程保存路径(直接回车使用默认路径:kc_selected.hylee):\n").strip()
                if x == "":  # 直接回车
                    selected_causes = self.load_selected_cause()
                else:
                    selected_causes = self.load_selected_cause(file_path=x)
            elif x == "3":
                x = input("请输入想退选课程前面的编号:\n").strip()
                try:
                    x = int(x)
                    if (x < 1) or (x > len(selected_causes)):
                        print("输入有误")
                    else:
                        print("要退选以下课程吗？")
                        item = selected_causes[x - 1]
                        print(str(x), item.get("kcmc"), item.get("xf"), item.get("jsxx"),
                              item.get("sksj"), item.get("kch_id"),
                              item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
                        x = input("1.确定\n2.取消\n").strip()
                        if x == "1":  # 退选课程
                            params = self.get_withdraw_params(username, item, url)
                            self.session.post(url, data=params)
                            unsubscribe_url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_tuikBcZzxkYzb.html?gnmkdm=N253512&su=" + username
                            r = self.session.post(unsubscribe_url,
                                                  data=self.get_unsubscribe_params(item, unsubscribe_url))
                            if r.text == "1":
                                print("退选课程成功")
                            else:
                                print(r.text)
                except:
                    print("输入有误")
            elif x == "#":
                break
            else:
                print("请输入合法操作")

    def get_unsubscribe_params(self, cause, url):
        # rwlx rlkz rlzlkz xklc
        params = {"kch_id": cause.get("kch_id"), "kcmc": cause.get("kcmc"), "jxb_ids": cause.get("jxb_id"),
                  "rwlx": self.modules[self.cause_type][2], "rlkz": self.modules[self.cause_type][3],
                  "rlzlkz": self.modules[self.cause_type][4], "xklc": self.modules[self.cause_type][5],
                  "xkxnm": self.public_params.get("xkxnm"), "xkxqm": self.public_params.get("xkxqm"), "txbsfrl": "0"}
        print(url + "需要提交的参数为:")
        print(params)
        return params

        # 从网络获取已经选择的课程信息并保存到文件中

    def get_selected_causes(self, selected_causes_file_path="kc_selected.hylee"):
        # if self.public_params is None:
        #     self.init_modules_and_params(module_from_file=module_from_file, module_file_path=module_file_path)
        username = input("请输入学号:\n")
        url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbChoosedDisplay.html?gnmkdm=N253512"
        params = {"xh_id": username.strip()}
        params = dict(params, **self.public_params)
        print(url + "需要提交的参数为:")
        print(params)
        r = self.session.post(url, data=params)
        data = json.loads(r.text)
        print(len(data))
        selected_causes = []
        count = 1
        for item in data:
            selected_cause = {"kcmc": item.get("kcmc"), "xf": item.get("xf"), "jsxx": item.get("jsxx"),
                              "sksj": item.get("sksj"), "kch_id": item.get("kch_id"),
                              "jxb_id": item.get("jxb_id"), "xxkbj": item.get("xxkbj"), "cxbj": item.get("cxbj")}
            selected_causes.append(selected_cause)
            print(str(count), item.get("kcmc"), item.get("xf"), item.get("jsxx"),  # 检验结果是否正确
                  item.get("sksj"), item.get("kch_id"),
                  item.get("jxb_id"), item.get("xxkbj"), item.get("cxbj"))
            count = count + 1
        with open(selected_causes_file_path, "w", encoding="utf-8") as file:  # 将获取到的已选课程保存到文件中
            file.write(json.dumps(selected_causes))
        return selected_causes

    # 从文件中加载已选课程
    def load_selected_cause(self, file_path="kc_selected.hylee"):
        selected_causes = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                selected_causes = json.loads(line)
        count = 1
        for item in selected_causes:  # 打印信息检验是否正确
            print(str(count), item.get("kcmc"), item.get("xf"), item.get("jsxx"),
                  item.get("sksj"), item.get("kch_id"),
                  item.get("jxb_id"), item.get("xxkbj"),
                  item.get("cxbj"))
            count = count + 1
        return selected_causes
