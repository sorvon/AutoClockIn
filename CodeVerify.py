# coding:utf-8
# import re  # 用于正则
from PIL import Image  # 用于打开图片和对图片处理
from io import BytesIO
# import pytesseract  # 用于图片转文字
import requests
import base64
# from selenium import webdriver  # 用于打开网站
# import time  # 代码运行停顿


class VerificationCode:
    def __init__(self, secret_info: dict):
        self.response = requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode')
        self.codeToken = self.response.json().get('data').get('Token')
        self.secret_info = secret_info
        # self.driver = webdriver.Firefox()
        # self.find_element = self.driver.find_element_by_css_selector

    def get_pictures(self):
        # self.driver.get('http://123.255.123.3')  # 打开登陆页面
        # self.driver.save_screenshot('pictures.png')  # 全屏截图
        # page_snap_obj = Image.open('pictures.png')
        # img = self.find_element('#pic')  # 验证码元素位置
        # time.sleep(1)
        # location = img.location
        # size = img.size  # 获取验证码的大小参数
        # left = location['x']
        # top = location['y']
        # right = left + size['width']
        # bottom = top + size['height']
        # image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
        # image_obj.show()  # 打开切割后的完整验证码
        # self.driver.close()  # 处理完验证码后关闭浏览器
        # return image_obj

        img = requests.get('https://fangkong.hnu.edu.cn/imagevcode?token={token}'.format(token=self.codeToken))
        Image.open(BytesIO(img.content))
        return Image.open(BytesIO(img.content))
        # return Image.open("codeCache.jpg")

    def processing_image(self):
        image_obj = self.get_pictures()  # 获取验证码
        img = image_obj.convert("L")  # 转灰度
        pixdata = img.load()
        w, h = img.size
        threshold = 180
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img

    def delete_spot(self):
        images = self.processing_image()
        # data = images.getdata()
        # w, h = images.size
        # black_point = 0
        # for x in range(1, w - 1):
        #     for y in range(1, h - 1):
        #         mid_pixel = data[w * y + x]  # 中央像素点像素值
        #         if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
        #             top_pixel = data[w * (y - 1) + x]
        #             left_pixel = data[w * y + (x - 1)]
        #             down_pixel = data[w * (y + 1) + x]
        #             right_pixel = data[w * y + (x + 1)]
        #             # 判断上下左右的黑色像素点总个数
        #             if top_pixel < 10:
        #                 black_point += 1
        #             if left_pixel < 10:
        #                 black_point += 1
        #             if down_pixel < 10:
        #                 black_point += 1
        #             if right_pixel < 10:
        #                 black_point += 1
        #             if black_point < 1:
        #                 images.putpixel((x, y), 255)
        #             black_point = 0
        # images.show()
        return images

    # def image_str(self):
    #     image = self.delete_spot()
    #     pytesseract.pytesseract.tesseract_cmd = r"E:\Program Files (x86)\Tesseract-OCR\tesseract.exe"  # 设置pyteseract路径
    #     result = pytesseract.image_to_string(image)  # 图片转文字
    #     resultj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
    #     result_four = resultj[0:4]  # 只获取前4个字符
    #     # print(resultj)  # 打印识别的验证码
    #     return result_four

    def get_token(self):
        get_token = self.secret_info['get_token']
        response = requests.get(get_token)
        return response.json()['access_token']

    def image_str2(self):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
        # 二进制方式打开图片文件
        imgByteArr = BytesIO()
        self.delete_spot().save(imgByteArr, 'png')
        img = base64.b64encode(imgByteArr.getvalue())

        params = {"image": img}
        access_token = self.get_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        result_list = response.json()['words_result']
        result_str = ''
        for result_dict in result_list:
            result_str += result_dict['words']
        print(result_str)
        return result_str


