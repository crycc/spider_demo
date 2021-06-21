import requests
import re
from lxml import html
import random
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_proxies():
    """
    获取前5页代理地址，类型为HTTP,间隔1s防止触发反爬机制
    """
    proxies = []
    for page in range(1, 40):
        proxy_url = "http://www.kuaidaili.com/free/inha/{}".format(page)
        res = requests.get(url=proxy_url, headers=headers)
        tree = html.fromstring(res.text)
        tr_list = tree.xpath('//*[@id="list"]/table/tbody/tr')
        print(page)
        for i in range(len(tr_list)):
            ip = re.findall('\d+\.\d+\.\d+\.\d+', html.tostring(tr_list[i][0]).decode())[0]
            port = re.findall('\d+', html.tostring(tr_list[i][1]).decode())[0]
            full_ip = '{}:{}'.format(ip, port)
            type = re.findall('>\S+<', html.tostring(tr_list[i][3]).decode())[0][1:-1]
            if type == 'HTTP':
                proxies.append(full_ip)
            else:
                print("{}:{}".format(type, full_ip))
        time.sleep(1)
    return proxies


def get_alive_proxies(url):
    """
    用目标网址进行连接测试，剔除失效的代理，筛选出的成功代理，写入本地文件
    """
    proxies = get_proxies()
    alive_proxies = []
    if os.path.exists('alive_proxies.txt'):
        print("已存在")
        os.remove('alive_proxies.txt')
    f = open('alive_proxies.txt', 'a')
    for proxy in proxies:
        try:
            r = requests.get(url=url, headers=headers, proxies={'http': proxy}, timeout=3)
            if r.status_code == 200:
                alive_proxies.append(proxy)
                f.write(proxy + '\n')
            else:
                print("代理失效:{}".format(proxy))
        except:
            print("代理失效:{}".format(proxy))
    f.close()

def spider():
    url="http://httpbin.org/get?show_env=1"
    with open('alive_proxies.txt','r') as f:
        lines = f.readlines()
        proxys = list(map(lambda x: x.strip(), [y for y in lines]))
    # res=requests.get(url=url,proxies={'HTTP': random.choice(proxys)})
    res=requests.get(url=url,proxies={'http':'113.237.3.178:9999'})
    tree = html.fromstring(res.text)
    # tr_list = tree.xpath('//*[@id="leftinfo"]/div[3]/div[2]/div[2]/span[1]')
    # ip = re.findall('\d+\.\d+\.\d+\.\d+', html.tostring(tr_list[0]).decode())[0]
    ip=res.text
    print(ip)

if __name__ == "__main__":
    # //*[@id="leftinfo"]/div[3]/div[2]/div[2]/span[1]
    # get_alive_proxies("http://www.baidu.com/")
    spider()
