from setuptools import setup

setup(
    name='wxPush',  # 需要打包的名字,即本模块要发布的名字
    version='v2.0',     # 版本
    description='推送给我个人微信的消息',  # 简要描述
    py_modules=['wx_send', 'savetext'],   #  需要打包的模块
    author='Haoj', # 作者名
    author_email='hajmail2000@163.com',   # 作者邮件
    # url='https://github.com/vfrtgb158/email', # 项目地址,一般是代码托管的网站
    requires=['requests', 'threading', 'json', 'savetext'], # 依赖包,如果没有,可以不要
    license='MIT'
)