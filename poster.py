#!/usr/bin/env python
#coding=utf-8
import time
import random

import requests
import simplejson as json
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import smtplib
from email.mime.text import MIMEText


def send_sms():
    sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
    ssender = SmsSingleSender("", "")
    try:
        result = ssender.send(sms_type, 86, "1831110xxxx",
                              "啊,这是一条测试短信,抓取科一考试信息的时间段", extend="", ext="456")
    finally:
        pass



def send_email(date):
    if send_mail(mailto_list, "可以科一考试在周末", "可以考试的时间为: %s"%date):
        print("发送email成功")
    else:
        print("发送email失败")


def check_in_happy_date(date):
    happy_date = ["2018-05-26", "2018-05-27", "2018-06-02", "2018-06-03"]
    if date in happy_date:
        send_email(date)
        return True
    else:
        return False


def get_exam_info():
    url = "http://bj.122.gov.cn/m/examplan/getExamPlanDetail"

    querystring = {"fzjg": "%E4%BA%ACA", "kskm": "1", "ksdd": "110043A", "kscx": "C1", "startTime": "2018-05-15",
                   "endTime": "2018-07-15", "zt": "0"}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "8212c131-ebf7-4e6e-8509-59e891f6c1e3"
    }

    response = requests.request("POST", url, headers=headers, params=querystring)
    data = json.loads(response.text)["data"]
    for i in data:
        date = i["ksrq"]
        if check_in_happy_date(data): break


mailto_list = ["1831@139.com"]
mail_host = "smtp.139.com"  # 设置服务器
mail_user = "1831121@139.com"  # 用户名
mail_pass = "573384"  # 口令
mail_postfix = "139.com"  # 发件箱的后缀


def send_mail(to_list, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content, _subtype='html', _charset='gb2312')  # 创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub  # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception as e:
        return False



while True:
    get_exam_info()
    random_int = random.uniform(3,10)
    time.sleep(random_int)
