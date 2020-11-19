#--coding:utf-8--

import requests
from lxml import etree

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
'Cookie': 'uuid=02656d12-f65b-4048-a5ae-0a06a8056137; ganji_uuid=4811484271022069787669; antipas=98n3f9i321ts73A9uK0129LR4; clueSourceCode=10103000312%2300; user_city_id=204; sessionid=65045cf7-2c95-40d3-8fee-0223b6c02746; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A83834068159%7D; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22ca_i%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2202656d12-f65b-4048-a5ae-0a06a8056137%22%2C%22sessionid%22%3A%2265045cf7-2c95-40d3-8fee-0223b6c02746%22%7D; preTime=%7B%22last%22%3A1555049972%2C%22this%22%3A1552292773%2C%22pre%22%3A1552292773%7D; cityDomain=wh'
}
#获取详情页面url
def get_detail_urls(url):
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    ul = html.xpath('//ul[@class="carlist clearfix js-top"]')[0]
    # print(ul)
    lis = ul.xpath('./li')
    detail_urls = []
    for li in lis:
        detail_url = li.xpath('./a/@href')
        detail_url = 'https://www.guazi.com' + detail_url[0]
        # print(detail_url)
        detail_urls.append(detail_url)
    return detail_urls

#解析详情页面内容
def parse_detail_page(url):
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    title = html.xpath('//div[@class="product-textbox"]/h2/text()')[0]
    title = title.replace(r'\r\n', '').strip()
    # print(title)
    info = html.xpath('//div[@class="product-textbox"]/ul/li/span/text()')
    # print(info)
    infos = {}
    cardtime = info[0]
    km = info[1]
    displacement = info[2]
    speedbox = info[3]

    infos['title'] = title
    infos['cardtime'] = cardtime
    infos['km'] = km
    infos['displacement'] = displacement
    infos['speedbox'] = speedbox
    return infos

#保存数据
def save_data(infos,f):

    f.write('{},{},{},{},{}\n'.format(infos['title'],infos['cardtime'],infos['km'],infos['displacement'],infos['speedbox']))


def main():
    #第一个url
    base_url = 'https://www.guazi.com/cs/buy/o{}/'
    with open('guazi_cs.csv', 'a', encoding='utf-8') as f:

        for x in range(1,6):
            url = base_url.format(x)
            #获取详情页面url
            detail_urls = get_detail_urls(url)
            #解析详情页面内容
            for detail_url in detail_urls:
                infos = parse_detail_page(detail_url)
                save_data(infos,f)

if __name__ == '__main__':
    main()




