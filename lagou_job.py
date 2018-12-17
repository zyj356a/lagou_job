import requests
import codecs
import time
import csv
import hashlib
from lxml import etree

URL = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'

cookie = {
    'Cookie': "JSESSIONID=ABAAABAAAFCAAEGB589C50ED3861EDFC58B82CC586EACA1; _ga=GA1.2.703366215.1543736379; _gid=GA1.2.455513277.1543736379; user_trace_token=20181202153939-6cd2b306-f605-11e8-890a-525400f775ce; LGUID=20181202153939-6cd2b6d0-f605-11e8-890a-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543736379; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221677402c75f681-095f250b805602-6313363-2073600-1677402c760b7b%22%2C%22%24device_id%22%3A%221677402c75f681-095f250b805602-6313363-2073600-1677402c760b7b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _putrc=1D4D1D25693D3DE2; login=true; unick=%E5%BC%A0%E7%86%A0%E6%9D%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=7; gate_login_token=adf56bbf53f784dfc3c203a455e490d759b09de7f04f8fe0; LGSID=20181204142009-a68239ab-f78c-11e8-89f3-525400f775ce; index_location_city=%E5%B9%BF%E5%B7%9E; TG-TRACK-CODE=search_code; SEARCH_ID=273d0e7315954551a2ad058e0ded7929; LGRID=20181204145614-b11e8971-f791-11e8-8a16-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543906574"
}

data = {
    'first': 'true',
    'pn': '1',
    'kd': 'python'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
}


def get_json():

    #para = {'city': '%E5%B9%BF%E5%B7%9E', 'needAddtionalResult': 'false'}
    page_lagou = requests.post(URL, headers=headers, data=data, cookies=cookie)
    # print(page_lagou.url)

    # 状态检测
    if page_lagou.status_code == 302 or page_lagou.status_code == 301:
        proxy, auth = get_proxy()
        proxy_header = headers
        proxy_header["Proxy-Authorization"] = auth
        page_lagou = requests.post(
            URL, headers=headers, data=data, cookies=cookie, proxies=proxy)

    page_lagou.encoding = 'utf-8'
    json_content = page_lagou.json()
    job_info = json_content['content']['positionResult']['result']
    return job_info


def process_info():
    with codecs.open("test.csv", 'wb', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(1, 29):
            data['pn'] = i
            job_info = get_json()
            for job in job_info:
                writer.writerow(
                    [job['companyFullName'], job['positionName'], job['businessZones'], job['salary']])

            time.sleep(5*3)


def get_proxy():

    orderno = "ZF20179xxxxxxxxx"
    secret = "3f9c2ecac7xxxxxxxxxxxxxxxx"

    ip = "forward.xdaili.cn"
    port = "80"

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))                # 计算时间戳
    string = ""
    string = "orderno=" + orderno + "," + "secret=" + \
        secret + "," + "timestamp=" + timestamp

    string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
    sign = md5_string.upper()                              # 转换成大写
    print(sign)
    auth = "sign=" + sign + "&" + "orderno=" + \
        orderno + "&" + "timestamp=" + timestamp

    print(auth)
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

    return proxy, auth


def main():
    process_info()


if __name__ == "__main__":
    main()
