# 案例内容

```python
# 1 登录酒仙app，预约茅台
	酒仙app-->登录--》预约茅台
    整体抢购流程（很多用户--》批量预约）
    	1 登录 （ddddocr识别图片验证码）
        2 提前预约
        3 到时间抢购
# 2 frida反调试
# 3 app壳与脱壳
```

# 抓包分析

```python
# 1 用户名密码登录
# 2 发送验证码
	-获取图片验证码
    -发送手机验证码
# 3 手机号+验证码登录
# 4 预约接口
```

```python
# 地址
	https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm
# 请求方式
	post
# 请求头
	无特殊
# 请求体
    appKey	a4feb647-7e15-35d2-8aa2-79ea171fb707
    deviceIdentify	a4feb647-7e15-35d2-8aa2-79ea171fb707
    ----uuid----
    pushToken	As2_lpWpxHeRH97ApKeO5wmyxXdDzHih8BxPPiSl39S1
    ----以上可能需要破----
    appVersion	9.1.13 # app版本
    areaId	500        # 地区id
    channelCode	0
    cpsId	tencent
    deviceType	ANDROID # 设备
    deviceTypeExtra	0
    equipmentType	Pixel 2 XL # 型号
    netEnv	wifi         # 网络环境
    passWord	abc*****123
    screenReslolution	1440x2712
    supportWebp	1
    sysVersion	11
    userName	181********
    
    
# 改包发现，appKey deviceIdentify pushToken 都可以去掉

```

## 密码登录

```python
## 代码实现登录（用户名+密码登录）---》登录成功后拿到token--》预约需要token


import uuid
import requests
def login_by_pwd(mobile, password, app_key, device_identify):
    res = requests.post(
        url="https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm",

        data={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "netEnv": "wifi",
            "passWord": password,
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "11",
            "userName": mobile
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "secure": "false",
        },
        verify=False
    )
    data_dict = res.json()
    print(res.text)

    token = data_dict['result']['userInfo']['token']
    return token


def run():
    app_key = device_identify = str(uuid.uuid4())
    mobile = "1234567890"
    password = "123456"

    token = login_by_pwd(mobile, password, app_key, device_identify)

    print(token+"登录成功")


if __name__ == '__main__':
    run()
```

![image-20240905193535573](C:\Users\tangb\Pictures\Screenshots\屏幕截图 2024-09-05 193512.png)

## 验证码登录

### 抓包分析

```python
### 1 获取图片验证码
### 2 使用ddddocr 循环识别成功
### 3 调用发送短信接口--》下发短信到手机 ：手机号+图片验证码
### 4 登录:手机号+短信验证码
```



```python
# 1 获取图片验证码
	-地址
    	https://newappuser.jiuxian.com/messages/graphCode.htm
    -请求方式
    	get
    -请求头
    	无特殊
    -请求参数
        appKey	a4feb647-7e15-35d2-8aa2-79ea171fb707
        deviceIdentify	a4feb647-7e15-35d2-8aa2-79ea171fb707
        pushToken	As2_lpWpxHeRH97ApKeO5wmyxXdDzHih8BxPPiSl39S1
        appVersion	9.1.13
        areaId	500
        channelCode	0
        cpsId	tencent
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        mobile	181*******
        netEnv	wifi
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        
    -返回值：
        {
        "result": {
            "imgCode":'base64编码'  # 验证码图片--》保存到本地即可
        },
        "errCode": "",
        "success": "1",
        "errMsg": ""
    	}
```

![image-20240605201728187](D:\app逆向and爬虫\day23-酒仙网\imgs\day23-酒仙网.assets\image-20240605201728187.png)

### 识别图片验证码方案ddddocr

```python
# 1 开源的ocr识别模块--》可以识别验证码
	-https://github.com/sml2h3/ddddocr
    -识别很多类型的验证码，具体看官网   
        
# 2 安装
pip3 install ddddocr

# 3 编写代码识别
import ddddocr

with open("v1.png", 'rb') as f:
    img_bytes = f.read()

ocr = ddddocr.DdddOcr(show_ad=False)
code = ocr.classification(img_bytes)

print(code)
```

### 验证码登录功能实现

```python
# 1 发送验证码接口
	-地址
    	https://newappuser.jiuxian.com/messages/mobileCode.htm
    -请求方式
    	get
    -请求参数
        appKey	a4feb647-7e15-35d2-8aa2-79ea171fb707
        appVersion	9.1.13
        areaId	500
        channelCode	0
        code	5800 # 识别通过的验证码
        cpsId	tencent
        deviceIdentify	a4feb647-7e15-35d2-8aa2-79ea171fb707
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        mobile	181*********
        netEnv	wifi
        pushToken	As2_lpWpxHeRH97ApKeO5wmyxXdDzHih8BxPPiSl39S1
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        type	1	
   

# 2 验证码登录接口
	-地址
    	https://newappuser.jiuxian.com/user/loginMobileFast.htm
    -请求方式
    	post
    -请求体
        appKey	a4feb647-7e15-35d2-8aa2-79ea171fb707
        appVersion	9.1.13
        areaId	500
        channelCode	0
        cpsId	tencent
        deviceIdentify	a4feb647-7e15-35d2-8aa2-79ea171fb707
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        mobile	181*********
        netEnv	wifi
        pushToken	As2_lpWpxHeRH97ApKeO5wmyxXdDzHih8BxPPiSl39S1
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        verifyCode	659476  # 手机验证码
```

```python
import requests
import uuid
import base64
import ddddocr


def fetch_image_code(mobile, app_key, device_identify):
    res = requests.get(
        url="https://newappuser.jiuxian.com/messages/graphCode.htm",
        params={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "4"
        },
        headers={
            "secure": "false",
            "Accept-Encoding": "gzip",
            'user-agent': "okhttp/3.14.9",
            'Host': "newappuser.jiuxian.com",
            'Connection': "keep-alive"
        },
        verify=False
    )

    image_str = res.json()['result']["imgCode"]

    img = base64.b64decode(image_str)

    ocr = ddddocr.DdddOcr(show_ad=False)
    code = ocr.classification(img)
    return code


def check_image_code(mobile, code, app_key, device_identify):
    res = requests.get(
        url='https://newappuser.jiuxian.com/messages/mobileCode.htm',
        params={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "code": code,
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "1"
        },
        verify=False
    )
    data_dict = res.json()

    # {'result': '', 'errCode': '', 'success': '1', 'errMsg': ''}
    # {'result': '', 'errCode': '1200013', 'success': '0', 'errMsg': '验证码输入错误'}
    # print(data_dict)
    return data_dict.get('success') == "1"


def login_by_sms(mobile, sms_code, app_key, device_identify):
    res = requests.post(
        url="https://newappuser.jiuxian.com/user/loginMobileFast.htm",
        data={
            "appKey": app_key,
             "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "verifyCode": sms_code
        },
        verify=False
    )
    # {"result":"","errCode":"1200003","success":"0","errMsg":"验证码错误或已过期，请重新输入"}
    # {"result":{...},"errCode":"1200093","success":"1","errMsg":"初始化密码"}
    # {"result":{...},"errCode":"","success":"1","errMsg":""}
    data_dict = res.json()
    return data_dict.get("success") == "1", data_dict.get('result')


def run():
    mobile = "181********"
    app_key = device_identify = str(uuid.uuid4())
    while True:
        img_code = fetch_image_code(mobile, app_key, device_identify)
        status = check_image_code(mobile, img_code, app_key, device_identify)
        if status:
            break

    sms_code = input("请输入验证码：")

    status, data_dict = login_by_sms(mobile, sms_code, app_key, device_identify)
    if not status:
        print("登录失败")
        return
    print("登录成功")
    print(data_dict)


if __name__ == '__main__':
    run()


'''
{'userInfo': {'apiVersion': 1.0, 'areaId': 500, 'channelCode': '0', 'isClubUser': False, 'isNewUser': False, 'loginUnionFirst': 0, 'loginWay': 2, 'mobile': '181********', 'needBindMobile': False, 'rank': 1, 'rankName': '酒虫', 'sex': 0, 'token': '6494ac1cd90b462fbd3c953a69a70861210440860', 'uid': 210440860, 'uname': 'jxw485893769', 'userImg': 'https://misc.jiuxian.com/img/usercenter/sbbgg.jpg'}}

'''
```

## 密码登录 +预约茅台

### 抓包分析预约接口

```python
# 1 预约接口
	- 地址
    	-https://newappuser.jiuxian.com/reservation/preReservation.htm
    - 请求方式
    	get
    - 请求参数
        actId	2168
        appKey	a4feb647-7e15-35d2-8aa2-79ea171fb707
        appVersion	9.1.13
        areaId	500
        channel	1
        channelCode	0
        cpsId	tencent
        deviceIdentify	a4feb647-7e15-35d2-8aa2-79ea171fb707
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        netEnv	wifi
        productId	626626
        pushToken	As2_lpWpxHeRH97ApKeO5wmyxXdDzHih8BxPPiSl39S1
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        token	a4229ff7961e4e8bb22f8589e1c25d92210440860 #登录信息，token
    
```

```python
import requests

import requests
import uuid


def login_by_pwd(mobile, password, app_key, device_identify):
    res = requests.post(
        url="https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm",
        data={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "netEnv": "wifi",
            "passWord": password,
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "userName": mobile
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "secure": "false",
        },
        verify=False
    )
    data_dict = res.json()

    token = data_dict['result']['userInfo']['token']
    return token


def pre_reservation(token, app_key, device_identify):
    res = requests.get(
        url="https://newappuser.jiuxian.com/reservation/preReservation.htm",
        params={
            'actId': '1810',
            'appKey': app_key,
            'appVersion': '9.1.13',
            'areaId': '2707',
            'channel': '1',
            'channelCode': '0',
            'cpsId': 'tencent',
            'deviceIdentify': device_identify,
            'deviceType': 'ANDROID',
            'deviceTypeExtra': '	0',
            'equipmentType': 'Pixel 2 XL',
            'lati': '31.088975',
            'longi': '121.58378',
            'netEnv': 'wifi',
            'productId': '626626',
            # 'pushToken': 'AsLMhsufh3YEmpzPv3S5nHhv0pxuModssTVXvf1TSIsp',
            'screenReslolution': '1440x2712',
            'supportWebp': '1',
            'sysVersion': '11',
            'token': token
        },
        verify=False

    )

    data_dict = res.json()
    print(data_dict)


def run():
    app_key = device_identify = str(uuid.uuid4())
    mobile = "1234567890"
    password = "123456"
    token = login_by_pwd(mobile, password, app_key, device_identify)
    print(token)

    pre_reservation(token, app_key, device_identify)


if __name__ == '__main__':
    run()


 '''
 {'result': {'verificationState': False}, 'errCode': '1200601', 'success': '0', 'errMsg': '您已预约成功，不需重复预约'}
 
 '''




#  当前这个app，需要预约--》抢购
	-假设咱们有很多账号---》批量预约--》完成了
    -抢购：到时见  立即抢购--》抓包
    	-这个代码咱们没有写 （定时任务）
        -抢购不是速度快就能成---》后台有随机的逻辑--》这个咱们控制不了--》 后续完成后更新到库
        
# 还有些app，小程序--》只需要预约--》他们抽奖
	-针对于这种--》大家可以只预约--》抽奖成功--》通知
    -i茅台，很多第三方小程序--》抽中的概率很低
	
```

# frida反调试

## frida 反调试

```python
# 1 之前做app，有frida的反调试---》打印所有so文件---》删除检测frida的so文件
	-识货，得物。。。
    
# 2 有些app，不是这种机制，在运行的时候，检测frida的相关特征，检测到后就直接退出app----》不允许使用frida调试[进程，文件]--->酒仙app--》就是这种机制
	#Frida-Hook-app时候
    - 正常去运行APP，无额外的其他特征
    - 正常去运行APP + 运行frida进行Hook【在手机上会生成一个文件】
    有些app内部监测是否有这个文件，如果有这个文件，那么就让app强制停止，或不让hook成功
    
# 3 针对于这种情况，如何绕过

# 4 frida的增强版---》把frida名字改掉---》运行的时候--》没有frida的特征
	strongR-frida-android
    
# 5 它不针对所有app，只针对于 检测frida特征的app有效
    https://github.com/hzzheyang/strongR-frida-android/releases
    跟随 FRIDA 上游自动修补程序(frida 有哪个版本，它就有哪个版本，一一对应的)，并为 Android 构建反检测版本的 frida-server
    
    
# 6 当时使用frida-server时，是有版本的，并且版本要跟ptyhon模块一一对应
	-我们当时用的版本是：16.2.1
    -我们现在使用 strongR-frida-android[hluda]-->版本要跟之前的frida-server版本对应：16.2.1
# 7 我们下载：
	https://github.com/hzzheyang/strongR-frida-android/releases/download/16.2.1/hluda-server-16.2.1-android-arm64.xz
       
    
# 8 以后使用 hluda 替代 frida-server
```

![image-20240605214045671](D:/app逆向and爬虫/day23-酒仙网/imgs/day23-酒仙网.assets/image-20240605214045671.png)

##  绕过

```python
# 1 下载对应python frida模块版本：16.2.1--》》对应手机平台
# 2 解压-->把软件，推送到手机上
	adb push hluda /data/local/tmp/
# 3 修改权限
	chomd 777 h 
# 4 关于Linux 权限解释
	rwx   rwx   rwx
# 5 以后可以不使用frida-server了，以后就用hluda 当frida-server用即可
```

![image-20240605214547411](D:/app逆向and爬虫/day23-酒仙网/imgs/day23-酒仙网.assets/image-20240605214547411.png)



```python
# 如果运行 frida-server--》hook不到

# 运行  hluda --》hook到

import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.jiuxianapk.ui"])
session = rdev.attach(pid)

scr = """
console.log("======Start HOOK======");
Java.perform(function () {
    var LocaleData = Java.use("libcore.icu.LocaleData");

    LocaleData.getDateFormat.implementation = function(i){
        console.log('=====>',i);
        var res = this.getDateFormat();
        console.log('=====>',res);
    }
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)
sys.stdin.read()
```



# app脱壳

## 加壳原理

```python
# 1 把 酒仙app，拖到jadx中，发现反编译回来的代码很少
	-有些壳的特征：腾讯，邦邦，360。。。 包
# 2 加壳原理
	安卓开发：
    	java代码+sdk+JNI代码 ----》apk(java代码写的：dex，JNI代码：so文件  资源文件 xml)
    app加壳了
    	java代码+sdk+JNI代码--》使用第三方加壳工具(邦邦，360)---》把dex隐藏到 so文件--》dex很小，so很大
        
# 3 app 运行时
 app运行时：未加壳app
    把dex加载到内存中，执行了
    
  app运行时：加壳app
    先加载dex--》so文件加载进来---》dex都在so中--》逆操作--》从so中解出dex--》在内存中--》执行逻辑
  加壳后--》加载运行app--》速度慢--》大厂一般不加壳--》他们用非常强的加密方案，让咱们破解不了
  小公司--》没有很强的加密--》加壳，牺牲速度--》保证安全
    
    
# 4 脱壳方案(没有一种通用脱壳方案) app加壳，有很多代--》不同厂商加壳思路不一样
 	#手动脱壳（难度大）：
        通过动态调试，跟踪计算Dex源文件的内存偏移地址，从内存中Dump出Dex文件
        难度大，寄存器，汇编，反调试，反读写
    # 工具脱壳：
        HOOK技术/内存特征寻找
        简单易操作
        基于xposed 脱壳工具：
            Fdex2：Hook ClassLoader loadClass方法 通用脱壳
            dumpDex：https://github.com/WrBug/dumpDex
        基于frida的脱壳工具（咱们学习）：
            frida-dexdump：https://github.com/hluwa/FRIDA-DEXDump

        自己定制脱壳机--》aosp刷机后--》自己定制脱壳机
        armPro收费脱壳（花钱）
```

## frida-dexdump 脱壳

```python
## 使用步骤：
1 安装模块[电脑端]：
	pip install frida-dexdump
2 手机端启动frida-server，端口转发

3 执行脱壳命令即可
# frida-dexdump  -U -f 包名称
frida-dexdump -U -f com.jiuxianapk.ui 
frida-dexdump -U -d -f com.jiuxianapk.ui  # 深度脱壳

4 使用jadx打开下载后的dex即可

5 有时候一次性把dex拖进去会报错
	-某个dex可能不是这个app或这个dex有问题
    -一个个的把dex拖入，哪个报错，就把哪个删除
    -每个dex都可以反编译成一部分java，但是由于下载的dex，某个可能有问题导致整个项目都反编译不了，找出那个有错的dex把它删除即可
```



