"""
# File       : demo1.py
# Time       : 5:21 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import json
import re

import requests

import time

# from htmlcodes import html
movies_info = {}


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Cookie': '__mta=140860941.1679217705498.1679378135988.1679378230218.62; uuid_n_v=v1; uuid=77252F60C63711ED8E157D25D41D8686D88861FE8CED4A74AAB965BDB3DAE835; _lxsdk_cuid=186f92cc10e62-0ba71845d4e91c8-412f2c3d-1fa400-186f92cc10fc8; _lxsdk=77252F60C63711ED8E157D25D41D8686D88861FE8CED4A74AAB965BDB3DAE835; __mta=140860941.1679217705498.1679286747440.1679302508989.30; _csrf=d14e4b6b11aab30bac29d8ad4b101208a8024c55d523003f0d7f3da8672eb742; _lxsdk_s=18702bc66e6-8a6-29c-a08%7C%7C14'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html, is_top_rank):
    global movies_info
    re_exp = '<dd>.*?board-index.*?>(.*?)</i>' \
             '.*?data-src="(.*?)"' \
             '.*?title="(.*?)"' \
             '.*?star.*?>(.*?)</p>' \
             '.*?releasetime.*?>(.*?)</p>'
    if is_top_rank:
        re_exp += '.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>'
    else:
        re_exp += '.*?realtime.*?stonefont">(.*?)</span></span>' \
                  '.*?total-boxoffice.*?stonefont">(.*?)</span></span>'
    pattern = re.compile(re_exp,
                         # '<dd>.*?board-index.*?>(.*?)</i>'  # match borard-index
                         # '.*?data-src="(.*?)"'  # match img src
                         # '.*?title="(.*?)"'  # match movie title
                         # '.*?star.*?>(.*?)</p>'  # match movie main actors
                         # '.*?releasetime.*?>(.*?)</p>'  # match movie release time
                         # '.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',  # match movie rank now
                         re.S)
    items = re.findall(pattern, html)  # cause of mismatch rules that can't get data from url straint
    for i in range(len(items)):
        movies_info[i] = {
            'index': items[i][0],
            'image': items[i][1],
            'title': items[i][2].strip(),
            'actor': items[i][3].strip()[3:] if len(items[i][3]) > 3 else '',
            'time': items[i][4].strip()[5:] if len(items[i][4]) > 5 else '',
            'score': items[i][5].strip() + items[i][6].strip()
        }


def get_board4_data():
    global movies_info
    for i in range(10):
        url = 'https://www.maoyan.com/board/4?timeStamp=1679389056220' \
              '&channelId=40011&index=8' \
              '&signKey=3c1bafec44109cd5ed08b803c53d74ad' \
              '&sVersion=1&webdriver=false' \
              '&requestCode=55ebed6aa16504fa241fed1dcc00821ateyyn' \
              '&offset=' \
              + str(i * 10)
        html = get_one_page(url)
        parse_one_page(html, True)
        time.sleep(0.2)


def get_board_others_data():
    url = 'https://www.maoyan.com/board/2?' \
          'timeStamp=1679302508350&channelId=40011' \
          '&index=10&signKey=bff45e167cb8362abcdbcf4032037f97' \
          '&sVersion=1&webdriver=false&' \
          'requestCode=92e4ef3fb9ed9327b6b371af3375facfi2iva'
    html = get_one_page(url)
    parse_one_page(html, False)
    time.sleep(0.1)


def write_to_file():
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(movies_info, ensure_ascii=False) + '\n')


def main():
    get_board4_data()
    # get_board_others_data()
    # print(movies_info)
    if movies_info:
        write_to_file()


if __name__ == '__main__':
    main()
