import requests
import time
from lxml import etree
def ini_num(file):
    ids = []
    for i in file:
        line = i.strip().split()
        ids.append(line[0])
    return ids

def str_url(ids):
    urls =[]
    for id in ids:
        str1="https://ajax1.maizegdb.org/record_data/gene_data.php?id="
        str3="&type=overview"
        str = f'{str1}{id}{str3}'
        urls.append(str)
    return urls

def res(urls):
    zmays_id =[]
    for url in urls:
        print(url)
        r = requests.get(url=url)
        response = r.text
        html = etree.HTML(response)
        res = html.xpath('/html/body/a[5]/text()')
        zmays_id.append(res)
        time.sleep(2)
    return zmays_id

in_fl = open('tmp.txt',mode="r")
zmays_id1 = ini_num(file=in_fl)
url_all = str_url(zmays_id1)
res_id =  res(urls=url_all)
with open('aaa.txt',mode='w') as f:
    for i in res_id:
        f.write(i[0]+"\n")

