# -*- coding:utf-8 -*-
from datetime import datetime

# current_time = datetime.now().strftime("%H:%M:%S")
# print(current_time)


def print_log(save_text):
    with open("log.log", "a") as f:
        f.write(save_text)


def get_now_time():
    return datetime.now().strftime("%H:%M:%S")


def get_now_data():
    return datetime.now().date()


