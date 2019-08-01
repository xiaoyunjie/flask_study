# -*- coding:utf-8 -*-

"""
@Author     :   Browser
@file       :   tm.py
@time       :   2019/07/17
@software   :   PyCharm 
@description:   " "
"""



from app import app
from flask import Markup

@app.template_global()    #装饰器，注册为模板全局函数,自定义名称test
def bar():
    return '"I am bar!'

# 注册自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup('&#9835;')

# 注册自定义测试器
@app.template_test()
def abc(n):
    if n == 'home':
        return True
    return False


