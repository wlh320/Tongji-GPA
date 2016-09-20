#!python3

# 推荐windows下使用
import requests
import getpass
import os

# input id and password
print('同济大学成绩查询')
id = input('学号:')
password = getpass.getpass('密码(不回显):')

# login
login_url = 'http://tjis2.tongji.edu.cn:58080/amserver/UI/Login?service=adminconsoleservice&goto=http://tjis2.tongji.edu.cn:58080/amserver/base/AMAdminFrame&&IDToken1=' + \
    id + '&IDToken2=' + password + \
    '&aoJRw8EPYESWso6AoNBOiPGiOB4cXDI5wnkJkQ5OulHGOgQinGwwSLHwW8m2QpRGPniAFVAdzyIkUbmk'

# xuanke Wang check
check_url = 'http://xuanke.tongji.edu.cn/pass.jsp'

# get grade
grade_url = 'http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?link=/tj_xuankexjgl/score/query/student/cjcx.jsp?qxid=20051013779916$mkid=20051013779901&qxid=20051013779916'

# go and get grade!
session = requests.Session()
req1 = session.request("GET", login_url)
req2 = session.request("GET", check_url)
req3 = session.request("GET", grade_url)

# fuck GBK!
result = req3.text
head = result.find('</head>')
gbk = '<meta charset="GBK">'
result = result[0:head] + gbk + result[head:-1]

# Write to file
file = open('grade.html', 'w')
file.write(result)
file.close()
print('结果保存在当前目录下的grade.html.  Fuck it!')
os.system('pause')
