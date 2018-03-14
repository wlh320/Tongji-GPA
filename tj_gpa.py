#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
两年前写的太挫了，完全重构
"""
import os
import re
import sys
import getpass
import webbrowser
import requests


def input_info():
    """input id and password"""
    print('\t同济大学成绩查询\n')
    username = input('学号:')
    password = getpass.getpass('密码:')
    return username, password


def saml_login(session):
    """
    step:
    1. GET init_url    -> forward to sso_url
    2. GET sso_url     -> get a form and get sid_url
    3. POST sid_url    -> get login_url
    4. POST login_url  -> submit login data
    5. GET sid_url     -> get aseert_url
    5. POST assert_url -> 302 and then OK!
    """
    # 1
    base_url = 'https://ids.tongji.edu.cn:8443'
    init_url = 'http://xuanke.tongji.edu.cn:443/oiosaml/saml/login'
    res = session.get(init_url)

    # 2
    sso_url = re.findall(r'url=(.*)"><', str(res.content))[0]
    res = session.get(sso_url)

    # 3
    sid_url = base_url + re.findall(r'action="(.*)"><', str(res.content))[0]
    res = session.post(sid_url)

    # 4
    login_url = sid_url
    username, password = input_info()
    data = {
        'Ecom_Password': password,
        'Ecom_User_ID': username,
        'option': 'credential',
        'submit': '登录'
    }
    res = session.post(login_url, data)

    # 5
    sid_url = re.findall(r"top.location.href=\\'(.*)\\';", str(res.content))[0]
    res = session.get(sid_url)

    # 6
    assert_url = "http://xuanke.tongji.edu.cn:443/oiosaml/saml/SAMLAssertionConsumer"
    data = {
        'SAMLResponse': re.findall(r'value="(.*)"/>', str(res.content))[0]
    }
    res = session.post(assert_url, data)


def get_grade(session):
    """get grade!"""
    grade_url = ('http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?'
                 'link=/tj_xuankexjgl/score/query/student/cjcx.jsp'
                 '?qxid=20051013779916$mkid=20051013779901&qxid=20051013779916')
    req = session.request("GET", grade_url)

    # fuck GBK!
    result = req.text
    head = result.find('</head>')
    charset = '<meta charset="{}">'.format('GBK' if sys.platform == 'win32' else 'UTF-8')
    result = result[0:head] + charset + result[head:-1]

    # Write to file
    file = open('grade.html', 'w')
    file.write(result)
    file.close()
    print('--------------------------------\n结果保存在当前目录下的 grade.html')
    print('即将为您自动打开，请稍后 :)')
    webbrowser.open('grade.html')
    if sys.platform == 'win32':  # for windows user
        os.system('pause')


def main():
    """main"""
    try:
        session = requests.Session()
        saml_login(session)
        get_grade(session)
    except Exception as e:
        print('出错了, 请重试', e)


if __name__ == '__main__':
    main()
