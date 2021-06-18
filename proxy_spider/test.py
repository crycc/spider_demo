import requests
import re

url = "http://www.kuaidaili.com/free/inha/1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_result():
    res = requests.get(url=url, headers=headers)
    # print(res.text)
    with open("r.html", "wb+") as f:
        f.write(res.content)

    return res.text


def parse():
    text = get_result()
    # //*[@id="list"]/table/tbody/tr[1]/td[1]
    tr=re.compile(r'<tr>.*</tr>', re.S)
    td_ip = re.compile(r'<td data-title="IP">.*</td>', re.S)
    td_port = re.compile(r'<td data-title="PORT">.*</td>', re.S)
    td_form = re.compile(r'<td data-title="匿名度">', re.S)
    td_type = re.compile(r'<td data-title="类型">.*</td>', re.S)
    td_address = re.compile(r'<td data-title="位置">.*</td>', re.S)
    td_speed = re.compile(r'<td data-title="响应速度">.*</td>', re.S)
    td_time= re.compile(r'<td data-title="最后验证时间">.*</td>', re.S)
    list_tr = tr.findall(text)
    print(list_tr)


if __name__ == "__main__":
    parse()
