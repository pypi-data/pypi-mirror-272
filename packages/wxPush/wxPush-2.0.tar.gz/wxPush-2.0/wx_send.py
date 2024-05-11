#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import os
import threading
import savetext

import requests
# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()


# 定义新的 print 函数
def print(text, *args, **kw):
    """
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    """
    with mutex:
        _print(text, *args, **kw)

# 通知服务
# fmt: off
push_config = {
    'HITOKOTO': True,  # 启用一言（随机句子）

    'CONSOLE': False,  # 控制台输出

    'CHAT_ACCESS_TOKEN': 'OK',  # 微信开发平台token
    'APP_ID': 'wxde9579bfa36ba004',
    'APP_SECRET': '7ba4e2a3060a5d56742bd6241ce0ad86',
}

notify_function = []
# fmt: on

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v

def console(title: str, content: str) -> None:
    """
    使用 控制台 推送消息。
    """
    print(f"{title}\n\n{content}")

def wechat_test(title: str, content: str) -> None:
    """
    通过 个人微信公众号 推送消息。
    """
    body_jsons = [
        {
            "touser": "oB0ix6qF-Pip5YV9VWZGGsfUwmc4",
            "template_id": "Ax5UaBu6oJ_DybHKKGg_2-7u2kA5hrNYVPmEAVrQ1I4",  # 智慧水杯小程序
            "topcolor": "#FF0000",
            "data": {
                "thing1": {
                    "value": f"{title}",
                    "color": "#173177"
                },
                "amount2": {
                    "value": f"{content}",
                    "color": "#173177"
                },
                "time3": {
                    "value": f"{savetext.get_now_time()}",
                    "color": "#F80228"
                },
                "thing4": {
                    "value": f"无",
                    "color": "#F80228"
                }
            }
        },
        {
            "touser": "oB0ix6qF-Pip5YV9VWZGGsfUwmc4",
            "template_id": "oQuDVvE4oUeNZQoYtQ9lKI6Jb37Y0ptn_dPHAkgxQCA",  # 智慧水杯小程序
            "topcolor": "#FF0000",
            "data": {
                "thing1": {
                    "value": f"{title}",
                    "color": "#173177"
                },
                "thing2": {
                    "value": f"{content}",
                    "color": "#173177"
                },
                "time3": {
                    "value": f"{savetext.get_now_time()}",
                    "color": "#F80228"
                },
            }
        },
        {
            "touser": "oB0ix6qF-Pip5YV9VWZGGsfUwmc4",
            "template_id": "vaP-GAwjfdWXBjDgibmh0UWvQGIsXDy5LVylojWLucM",  # 智慧水杯小程序
            "url" : "http://vps-blog.aoj.lol",
            "data": {
                "thing1": {
                    "value": f"{title}",
                },
                "thing2": {
                    "value": f"{content}",
                },
                "time3": {
                    "value": f"{savetext.get_now_time()}",
                },
            }
        }
    ]
    if not push_config.get("CHAT_ACCESS_TOKEN"):
        print("个人微信公众号 服务的 个人微信公众号_TOKEN 未设置!!\n取消推送")
        return
    print("个人微信公众号 服务启动")
    access_token = chat_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)

    if title == "Haoj":
        body_json = body_jsons[0]
    elif title == "巴奴打卡":
        body_json = body_jsons[2]
    else:
        body_json = body_jsons[1]
    response = requests.post(url, json=body_json).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("个人微信公众号 推送消息成功")
    else:
        print(response)


def chat_get_access_token():
    ## 因为我是从文件中读取的，你们嫌麻烦可以直接把两个填到链接的大括号内，并删除后面的.format（xxx）
    # appId
    access_token = "NULL"
    app_id = push_config["APP_ID"]
    # appSecret
    app_secret = push_config["APP_SECRET"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    ## 尝试使用get获取并转换成json，同时取其中的值
    try:
        access_token = requests.get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
    # print(access_token)
    return access_token

def one() -> str:
    """
    获取一条一言。
    :return:
    """
    url = "https://v1.hitokoto.cn/"
    res = requests.get(url).json()
    return res["hitokoto"] + "    ----" + res["from"]

if push_config.get("CHAT_ACCESS_TOKEN"):
    notify_function.append(wechat_test)


def send(title: str, content: str) -> None:
    if not content:
        print(f"{title} 推送内容为空！")
        return

    hitokoto = push_config.get("HITOKOTO")

    text = one() if hitokoto else ""
    content += "\t\t" + text

    ts = [
        threading.Thread(target=mode, args=(title, content), name=mode.__name__)
        for mode in notify_function
    ]
    [t.start() for t in ts]
    [t.join() for t in ts]


def WxPusher_send_message(title="消息通知", content="测试消息", contentType=3, url='https://defalut.haoj.xyz'):
    url = 'https://wxpusher.zjiecode.com/api/send/message'
    headers = {'Content-Type': 'application/json'}

    data = {
        "appToken": "AT_0JgkmGIiHCWQ7Rv5upkOXSx6KibFB929",
        "content": content,
        "summary": title,
        "contentType": contentType,
        "uids": ["UID_IM7H6gD5nbBWRUNbIzXFfTGgQ4M2"],
        "url": url,
        "verifyPay": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print("Failed to send message:", e)

def main():
    send("title", "content")


if __name__ == "__main__":
    main()
