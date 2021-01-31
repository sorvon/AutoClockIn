# coding:utf-8
from CodeVerify import VerificationCode
import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S')
class ClockIn:
    def __init__(self, secret_info: dict):
        self.secret_info = secret_info
        self.verificationCode = VerificationCode(self.secret_info)
        self.num = self.verificationCode.image_str2()
        while len(self.num) != 4:
            self.verificationCode = VerificationCode(self.secret_info)
            self.num = self.verificationCode.image_str2()

    def login(self):
        loginData = {
            'Code': self.secret_info['loginData']['Code'],
            'Password': self.secret_info['loginData']['Password'],
            'WechatUserinfoCode': None,
            'VerCode': self.num,
            'Token': self.verificationCode.codeToken
        }
        headers = {
            'Host': 'fangkong.hnu.edu.cn',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://fangkong.hnu.edu.cn/app',
            'Accept': 'application/json,text/plain,*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-CN; Mi 10 Build/RKQ1.200710.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/4.3.0.142 Mobile Safari/537.36'
        }
        response = requests.post(url='https://fangkong.hnu.edu.cn/api/v1/account/login', data=json.dumps(loginData),
                                 headers=headers)
        # while response.json().get('code') != 0:
        #     response = requests.post(url='https://fangkong.hnu.edu.cn/api/v1/account/login', data=json.dumps(loginData),
        #                              headers=headers)

        if response.json().get('code') == 0:
            # print(response.cookies)
            # print(requests.utils.dict_from_cookiejar(response.cookies))
            setCookies = requests.utils.dict_from_cookiejar(response.cookies)

            postHeaders = {'Host': 'fangkong.hnu.edu.cn', 'Origin': 'https://fangkong.hnu.edu.cn',
                           'Content-Type': 'application/json;charset=UTF-8',
                           'Referer': 'https://fangkong.hnu.edu.cn/app', 'Connection': 'keep-alive',
                           'Accept': 'application/json,text/plain,*/*',
                           'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-CN; Mi 10 Build/RKQ1.200710.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/4.3.0.142 Mobile Safari/537.36',
                           'Cookie': 'TOKEN={token};.ASPXAUTH={aspxauth}'.format(token=setCookies.get('TOKEN'),
                                                                                 aspxauth=setCookies.get('.ASPXAUTH'))}

            postBody = self.secret_info['postBody']
            response = requests.post(url='https://fangkong.hnu.edu.cn/api/v1/clockinlog/add', data=json.dumps(postBody),
                                     headers=postHeaders)
        print(response.json())
        logging.info(response.json())
        return response.json()['code']
        # {'code': 0, 'data': None, 'msg': '成功'}
        # {'code': 1, 'data': None, 'msg': '今天已提交过打卡信息！'}


if __name__ == '__main__':
    secret_info_dict = json.loads(input())
    re_code = -1
    for i in range(0, 10):
        clockIn = ClockIn(secret_info_dict)
        re_code = clockIn.login()
        logging.info(re_code)
        if re_code == 0:
            exit(0)
        elif re_code == 1:
            print("打过卡了！")
            exit(0)
    exit(re_code)
