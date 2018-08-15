'''
这里作用是获取各个栏目的链接。
'''

import requests
from bs4 import BeautifulSoup
from config import *

#访问网站首页，返回源码
def get_index_page(url):
    index_page = requests.get(url)
    if index_page.status_code == 200:
        return index_page.text

#获取栏目链接，添加入列表。
def get_ChannelUrl(html):
    soup = BeautifulSoup(html,'lxml')
    Channel_lists = soup.select('.ym-submnu li span a')
    for item in Channel_lists:
        Channel_part = item.get('href')
        if Channel_part in EXIT_URL:
            print('排除抓取的频道:' + str(Channel_part))
        else:
            Channel_all = URL_HEAD + str(Channel_part)
            CHANNEL_URLS.append(Channel_all)
    return CHANNEL_URLS

if __name__ == '__main__':
    index_source = get_index_page()
    get_ChannelUrl(index_source)
