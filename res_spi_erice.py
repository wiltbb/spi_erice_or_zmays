from lxml import html as ht
import requests

def req_eRice(url, headers):
    etree = ht.etree
    r = requests.get(url=url, headers=headers)
    html_text = r.text
    html = etree.HTML(html_text, etree.HTMLParser())
    return html

def splice_context(td):
    texts = td.xpath("./text()")
    strong = td.xpath("./strong/text()")
    return texts[0].strip() + "[" + strong[0] + "]" + texts[1].strip()

def common(td):
    return td.xpath("./text()")[0].replace('\xa0', "").strip()

def location(td):
    return td.xpath("./a/text() | ./text() ")[0].replace('\xa0', "").strip()

def splic_1_or_3(tds):
    num = 0
    while num < len(tds):
        try:
            yield common(tds[num])
            num += 1
        except:
            yield  location(tds[num])
            num += 1

def res_1_or_3(tds):
    res_all = []
    for n in splic_1_or_3(tds):
        res_all.append(n)
    res_p1 = [res_all[i:i+7] for i in range(0,len(res_all),7)]
    for lst in res_p1:
        lst.pop()
    res_p2 = []
    for i in range(6,len(tds),7):
        strong = [splice_context(tds[i])]
        res_p2.append(strong)
    res = []
    for i in list(zip(res_p1,res_p2)):
        res.append(i[0]+i[1])
    return  res

def splic_2_or_4(tds):
    num = 0
    while num < len(tds):
        try:
            yield location(tds[num])
            num += 1
        except:
            yield  str(tds[num].xpath("./text()"))
            num += 1

def res_2_or_4(tds):
    res_all = []
    for n in splic_2_or_4(tds):
        res_all.append(n)
    res_sub = [res_all[i:i+13] for i in range(0,len(res_all),13)]
    for empty_str in res_sub:
        empty_str.remove('[]')
    return  res_sub

if __name__ == '__main__':
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    ele = req_eRice(
        url="http://www.elabcaas.cn/rice-cgi/Search_meth_results_5mc.cgi?chrs=chr1&pos_start=1&pos_end=100000&ziduan=nip-5mc", headers=headers)
    tds = ele.xpath("//*[contains(@class, 'right_words')]")
