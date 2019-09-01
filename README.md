>之前用过java实现选课功能，现在在学习python，所以想要用python也实现一下。
>本文仅供学习使用，请勿用于其他用途。
###### 首先打开 [数字广大](https://cas.gzhu.edu.cn/cas_server/login)
###### 然后打开浏览器开发者工具输入账号密码登录广大主页，查看请求头信息，Content-Type为application/x-www-form-urlencoded,如下图所示
![登录请求方式](https://img-blog.csdnimg.cn/20190901115613674.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 查看登录请求的url以及所需要提交的参数
![查看登录所需要的参数](https://img-blog.csdnimg.cn/2019090111571446.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 请求参数在上一个请求的网页中获得，也就是数字广大的html源码上可以获得
![登录参数特征](https://img-blog.csdnimg.cn/20190901115437215.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 查看登录参数与网页源码对应关系
![登录所需要提交的参数对应表](https://img-blog.csdnimg.cn/20190901115700742.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
```python
    #根据上面图片的特征通过html源码截取登录参数
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
```
###### 项目中用到requests库,用requests库中的session可以很自动处理cookie，所以在整个过程中需要保持用同一个session
```python
 #获取session的方法
 def get_session(self, file="cookies.hylee"):  # 获取当前会话，通过session可自动管理cookie
        if self.session is None:
            self.session = requests.Session()
            self.session.cookies = HC.LWPCookieJar(filename=file)
            headers = {
                # "Content-Type": "application/x-www-form-urlencoded",  # post请求默认类型，可以不加
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
            self.session.headers.update(headers)
        return self.session
```
###### 执行登录操作
```python
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
```
###### 为了在选课的时候不用频繁的登录和获取课程，在本项目中会把cookie和获取到的课程保存到本地，之后需要的话可以直接加载进来而不需要重新获取
```python
    #从文件中加载cookie信息，并添加到session中
    def load_cookies(self, file_path="cookies.hylee"):
        self.session = requests.session()
        self.session.cookies = HC.LWPCookieJar(filename=file_path)
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("cookie文件不存在") 
```
###### 登录成功以后会跳转到广大主页，直接点击教务系统的话会在新窗口打开，这样chrome浏览器就不能抓到数据包，所以要修改网页源码，将target属性去掉，使其在原来的标签页打开，具体步骤看下面的截图
![广大主页](https://img-blog.csdnimg.cn/20190901115642310.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
![自主选课url](https://img-blog.csdnimg.cn/20190901115720393.png)




![在这里插入图片描述](https://img-blog.csdnimg.cn/20190901115648458.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 去掉target属性以后点击教务系统，并抓取数据包，第一个url即为教务系统的url
![登录教务系统的url](https://img-blog.csdnimg.cn/20190901115622694.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 获取教务系统url地址后直接通过session访问教务系统登录
```python
	    r = self.session.get("http://jwxt.gzhu.edu.cn/sso/lyiotlogin")  # 登录教务系统
        if r.text.find("广州大学教学综合信息服务平台") != -1:
            print("登录教务系统成功")
            self.session.cookies.save(ignore_discard=True, ignore_expires=True)
            self.get_cause_types()
        else:
            print("登录教务系统失败")
```
###### 登录教务系统以后点击自主选课
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190901115617972.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 查看自主选课html网页源代码，可以知道不同课程有不同的特征值，而且每个年级都不一样
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190901115606161.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 根据上面的网页源码获取课程类型的特征信息，并保存到文件中，下次可以直接从本地文件中获取数据
```python
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
```
###### 可以通过本地文件或者访问教务系统获得课程类型特征信息
```python
    # 选课初始化参数和模块
    def init_modules_and_params(self, module_from_file=False, module_file_path="modules.hylee"):
        select_cause_url = "http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default"  # 点击自主选课请求的url
        self.html = self.session.get(select_cause_url).text  # 获取自主选课html页面
        if module_from_file is True:  # 本地加载课程类型
            self.load_modules(module_file_path)
        else:
            self.modules = self.get_modules(self.html)  # 获取课程的类型 体育 选修 主修
        self.public_params = self.get_public_params(self.html)  # 自主选课页面有的参数,一般每次请求都要加上
```
###### 点击查询按钮以后可以查看相应的数据包查看请求url以及需要提交的参数等信息
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190901115634925.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)
###### 具体实现代码请转到我的[github](https://github.com/HyLee-LHY/gzhu-causes-spider)项目查看，扫描下面二维码可以查看我的个人博客主页![个人博客](https://img-blog.csdnimg.cn/201909011151482.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0h5TGVlX0xIWQ==,size_16,color_FFFFFF,t_70)