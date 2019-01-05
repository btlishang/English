#-*- coding:utf-8 _*-
#
#  File Name:    phrases_spider
#  Author :      lishang
#  date：        2019/1/3
#
import requests,re,os
from pyquery import PyQuery as pq
from multiprocessing import Pool

base_url = "https://www.englishspeak.com"
# mac 目录
base_dir = "/Users/lishang/data/phrases/"
# win 目录
# base_dir = "G:\data/english-phrases/"
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
    # 计数
    num = 0
    for data in datas:
        info = pq(data.html())
        msg = data.html()
        f = info('.test')
        # 英文短语
        phrases = f.text().strip()
        result = re.search("</a>.*?</p>(.*?)</td>.*?phrases/mp3/(.*?)'\)",msg,re.S)
        if result:
            # 中文翻译
            phrases_cn = result.group(1).strip()
            # 英文mp3名称
            audio_name = result.group(2).strip()
            # 英文短语链接
            phrases_url = "http://dcgm6jfwtvdqr.cloudfront.net/instantspeak/english/phrases/mp3/" + audio_name
            # 计数
            num+=1
            # 下载音频
            get_audio(cate,audio_name,phrases_url)
            print(phrases,phrases_cn,phrases_url)
        else:
            print(result,"为空")
    print(cate,"总计：",num)

# 获取所有分类，并调用抓取方法
def get_url():
    url = "https://www.englishspeak.com/zh-cn/english-phrases";
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
    with open(base_dir + cate + '/' + name,'wb') as f:
        f.write(requests.get(url,headers=header).content)


if __name__ == '__main__':
    get_url()
