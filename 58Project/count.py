from time import sleep
from get_Products_info import *

'''
每十秒钟反馈mongo中的数据抓取情况。
目前是用Termimal开启的。
'''
def count():
    while True:
        print('目前mongo中详情页的链接有' + str(links_table.find().count()) + '条记录，' + '宝贝信息' + str(product_table.find().count()) + '条')
        sleep(20)

if __name__ == '__main__':
    count()