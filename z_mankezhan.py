#漫画栈漫画抓取
#抓取地址 https://www.mkzhan.com

# 第一步：导入第三方包
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
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
    # 2.4 返回获得网页
    return response.text

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
    lists = sel.find_all("div", 'rd-article__pic')
    count = 1
    for list in lists:
        img_url = list.find('img').get('data-src')
        img_name = dirName + '/U-%s.jpg' % count
        count = count + 1
        if not os.path.exists(img_name):
            content = get_img(img_url)
            if content:
                with open(img_name, 'wb') as f :
                    f.write(content)
                    # 以二进制的方式写入数据
                    print(img_name + "下载完毕")
        else:
            print("图片存在----"+img_name)
    #


# 主函数，程序的入口
def main(url):
    text = _get(url)
    sel = BeautifulSoup(text, 'lxml')
    title = sel.find('p','comic-title').string
    cove = sel.find('img','lazy').get('data-src')
    count = 0
    lenght = len(sel.find_all("li","j-chapter-item"))
    sater  = sel.find('div','de-chapter__title').find('span').string
    state = 1 if sater == "完结" else 0 #是否完结
    category = sel.find('div','comic-status').find('b').string #分类
    author = sel.find('div','comic-author').find('span','name').find('a').string #作者
    synopsis = sel.find('div','comic-intro').find('p','intro').string #简介

    content = get_img(cove)
    cove_path = "public/Cartoon/%s" % (title)
    img_name = cove_path + '/cover.jpg'
    if not os.path.exists(cove_path):
        os.makedirs(cove_path)

    with open(img_name, 'wb') as f:
        f.write(content)
        # 以二进制的方式写入数据
        print(img_name + "下载完毕")

    for li in sel.find_all("li","j-chapter-item"):
        chapat_url = li.find('a','j-chapter-link').get('data-hreflink')
        noli = str(li.find('a','j-chapter-link'))
        dr = re.compile(r'<[^>]+>',re.S)
        chapat_name = dr.sub('',noli)
        chapat_name = chapat_name.replace(noli,'').replace(' ','').replace("\n",'')

        path = "public/Cartoon/%s/%s-" %(title,lenght-count)
        count = count +1;
        dirName = u"{}".format(path +chapat_name)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        chapter("https://www.mkzhan.com" + chapat_url, dirName)



# 执行主函数
if __name__ == '__main__':
    # https: // www.lieqiman.com /
     main("https://www.mkzhan.com/213318/")
