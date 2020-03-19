import requests
from bs4 import BeautifulSoup
import os
import time

referer0 = 'http://www.qdaily.com/policy.html'
url = 'http://www.qdaily.com/labs.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": referer0,
}

# 进行网页请求
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
html = r.text
# 对网页文本进行解析
soup = BeautifulSoup(html, 'html.parser')

# 在主页寻找合适的文章链接地址 寻找含/paper前缀的链接
grid_list = soup.find_all('a', class_="com-grid-paper small")
# List Comprehensions 列表解析
link_list = [x['href'] for x in grid_list if x['href'].split('/')[1] == 'papers']
# 将网页前缀补全
prefix = "https://www.qdaily.com"
link_list = [prefix + x for x in link_list]

# 循环每个从首页获取的次级链接
for i, link in enumerate(link_list):

    # 利用链接访问网页并解析
    headers['Referer'] = url
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # 定位到具体的层级
    div = soup.find_all('div', class_='paper-detail-bd')[0]
    title = soup.find_all('title')[0].text
    title = title.split('_')[0]
    all_pic_li = div.find_all('li', class_='option')

    print("{}/{} working on {}".format(i, len(link_list), title))

    # 利用request访问每个data-src的链接并将文件下载到本地
    for child in all_pic_li:
        img_link = child.find('img')['data-src']
        img_name = list(child.children)[-1].text
        img_name = img_name.replace('/', '_')

        headers['Referer'] = link
        r_img = requests.get(img_link, headers=headers)

        path = './pic/{}/'.format(title)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + '{}.gif'.format(img_name), 'wb') as f:
            f.write(r_img.content)
            time.sleep(2.3333)  # 保持低爬取频率
