#-*- coding:utf-8 _*-
#
#  File Name:    spider
#  Author :      龙杯
#  date：        2019/1/2
#
import requests,re,os
from pyquery import PyQuery as pq

base_url = "https://www.englishspeak.com"
# mac 目录
#base_dir = "/Users/lishang/PycharmProjects/English/"
# win 目录
base_dir = "G:\data/english-words/"
header = {
        "cookie": "__cfduid=d0f6732e7eacfefe63c0d4a2644f25a8b1546408511; _ga=GA1.2.1654143687.1546408515; _gid=GA1.2.873369146.1546408515; __stripe_mid=cd4b5e10-27c4-4877-aad2-8c8e00709d3e; _englishspeak_r_session=U1RIRTFBc0h3a05sRlFERkx4RVZzWmlYYmtMUWIvbG5uNGNocUYwZjRrUWJGRG83amx2UWIyK1pkejBxQUYrOE91MWNrbDYzWXR1WEo3OVhubzFlUHpDNDFPZUVqMG9aSUhXL3pwcmR2NVRjTFRYTzFTeG5zQkU4RVNUa3RJNm81RkJCaHpFU0pIN3JiQWUxT0NqcjF3PT0tLTRFYlFMdnZaeGsvVnFkOXlPNDBzMVE9PQ%3D%3D--d730a66b9f25588ddbd75184b369ed82cd83cf56",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3608.4 Safari/537.36"
}
# 抓取单个分类下的所有数据
def get_info(url,cate):
    html = requests.get(url, headers=header)
    doc = pq(html.text)
    datas = doc('.table.table-striped tbody tr').items()
    print("当前分类为:",cate)
    num = 0
    for data in datas:
        info = data.html()
        result = re.search("<a style.*?\('(.*?)'\)\">(.*?)</a>.*?</p>(.*?)</td>",info,re.S)
        if result:
            word_url = result.group(1).replace('?','')
            word = result.group(2).strip().replace('?','')
            word_cn = result.group(3).strip()
            num+=1
            # 下载音频
            get_audio(cate,word,word_url)
            print(word,word_cn,word_url)
        else:
            print(result,"为空")
    print(cate,"总计：",num)

# 获取所有分类，并调用抓取方法
def get_url():
    url = "https://www.englishspeak.com/zh-cn/english-words?category_key=1";
    html = requests.get(url,headers=header)
    doc = pq(html.text)
    datas = doc('.col-sm-12 ol li a').items()
    for data in datas:
        cate = data.text()
        url = base_url + data.attr('href')
        # print(cate,url)
        # 按类别新建目录
        os.mkdir(base_dir + cate)
        get_info(url,cate)

# 下载音频到指定目录
def get_audio(cate,name,url):
    with open(base_dir + cate + '/' + name + '.mp3','wb') as f:
        f.write(requests.get(url,headers=header).content)


if __name__ == '__main__':
    get_url()