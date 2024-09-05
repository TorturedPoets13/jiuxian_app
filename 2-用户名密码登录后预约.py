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
    mobile = "1234567980"
    password = "123456"
    token = login_by_pwd(mobile, password, app_key, device_identify)
    print(token)

    pre_reservation(token, app_key, device_identify)


if __name__ == '__main__':
    run()

'''
{'result': {'verificationState': False}, 'errCode': '1200601', 'success': '0', 'errMsg': '您已预约成功，不需重复预约'}

'''
