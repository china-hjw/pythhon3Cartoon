#猎奇漫画抓取
#抓取地址  https://www.lieqiman.com/

# 第一步：导入第三方包
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pinyin
import os
import re
import CartoonSql

# 第二步：获取目标网页
def _get(url):
    ua = UserAgent()
    # 2.2设置简单的反爬虫机制
    headers = {
        'User-Agent': ua.random}
    # 2.3 请求目标网页，拿取爬取网页的内容，并保存内容
    response = requests.get(url, headers=headers)
    html = response.text.encode("latin1").decode("gbk")

    # 2.4 返回获得网页
    return html

# 判断获取图片的状态码是否正确
def get_img(img_urls):
    # 4.2 请求图片的url
    response = requests.get(img_urls)
    # 4.3 如果状态码是200，代表获取正确的url，返回获取的网页
    if response.status_code == 200:
        return response.content

# 下载章节图片
def chapter(url,dirName):
    # 2.1 执行_get(url)方法,并传入url,保存为text
    text = _get(url)
    sel = BeautifulSoup(text, 'lxml')
    # 第一步  获取基本信息
    lists = sel.find("div", 'detailcontent1')
    if lists.find_all('img'):
        list_arr = lists.find_all('img')

        count = 1
        for list in list_arr:
            img_url = list.get('src')

            img_name = dirName + '/U-%s.jpg' % count
            count = count + 1
            if not os.path.exists(img_name):
                content = get_img(img_url)
                if content:
                    with open(img_name, 'wb') as f:
                        f.write(content)
                        # 以二进制的方式写入数据
                        print(img_name+"下载成功")
            else:
                print('已存在---'+img_name )
        #

# 主函数，程序的入口
def main(url):
    for i in range(142):
        a_url = "https://www.lieqiman.com/mh/xe/%s.html" % (i+5)
        try:
            text = _get(a_url)
            sel = BeautifulSoup(text, 'lxml')
            title = sel.find("div", 'wkboxr').find('b').string
            synopsis = sel.find("div", 'wikicon').find('p').string
            sql = CartoonSql.CartoonSql().Cartoon(
                name=title,
                state=1,
                category="猎奇",
                author="admin",
                synopsis=synopsis,
                curl=a_url,
                curl_type='z_lieqi',
            )
            list2s = sel.find_all("a", "album_link2")
            lenght = len(list2s) - 6
            count = 0
            for li in range(lenght):
                chapat_url = list2s[li].get('href')
                chapat_name = list2s[li].string
                path = "public/Cartoon/%s/%s-" % (title, lenght - count)
                count = count + 1
                dirName = u"{}".format(path + chapat_name)
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                chapter("https://www.lieqiman.com" + chapat_url, dirName)
        except:
            # 如果发生错误则回滚
            print("【【【【【【【【【【网页丢失】】】】】】】】】】】】】】】")



# 执行主函数
if __name__ == '__main__':
    # https: // www.lieqiman.com /
    main("https://www.lieqiman.com/")
