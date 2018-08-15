from multiprocessing.dummy import Pool
from get_ChannelUrl import *
import pymongo
from count import *

#MONGO数据库
mongo_client = pymongo.MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]
links_table = mongo_db[TABLE1]
product_table = mongo_db[TABLE2]

#get_ChannelUrl中的方法
index_source = get_index_page(INDEX_URL)
get_ChannelUrl(index_source)

#由栏目拼接URL，翻页。
def generate_urls(channel,category,pn):
    url = '{}{}/pn{}/'.format(channel,str(category),str(pn))
    print(url)
    response = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(response.text,'lxml')
    tip1 = soup.select('.noinfotishi')      #出现了tip1 或者tip2 都是没有宝贝的页面，可视为该类宝贝的结束。
    tip2 = soup.select('.ct')
    if tip1 or tip2:
        tip = 'None'        #tip作为页码结束的指标进行反馈
        return tip
    else:
        return response.text

#获取宝贝的详情页，并存储到mongodb
def prodect_detail_link(html):
    soup = BeautifulSoup(html,'lxml')
    links = soup.select('.tbimg tbody .zzinfo .img a')
    for item in links:
        link = item.get('href')
        if 'null' in link:
            get_product_info(link)
            links_table.insert({'detail_url':link})
            print('商品详情URL:'+ link +'保存至mongo成功!' )

#从宝贝的详情页获取宝贝信息，存储到mongodb
def get_product_info(url):
    response = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(response.text,'lxml')
    try:
        product_info = {
            'title': soup.select('.info_titile')[0].get_text(),
            'look_time':soup.select('.look_time')[0].get_text(),
            'wangt_person':soup.select('.want_person')[0].get_text(),
            'price':soup.select('.price_now')[0].get_text(),
            'location':soup.select('.palce_li span i')[0].get_text(),
            'description':soup.select('.baby_kuang p')[0].get_text()
        }
    except IndexError:
        print('有一些获取不到的东西')
    try:
        product_table.insert(product_info)
        print(product_info)
        print('该商品信息保存成功。')
    except:
        print('-----------保存失败-----------')


def main(channel):
    for i in range(1,101):
        html = generate_urls(channel,0,i)
        if html == 'None':
            print('已经是最后一页了...')
            break
        else:
            prodect_detail_link(html)

if __name__ == '__main__':
    pool = Pool(50)
    pool.map(main,[i for i in CHANNEL_URLS])

