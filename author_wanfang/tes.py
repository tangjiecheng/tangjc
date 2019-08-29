#
# def run():
#     # url = 'http://med.wanfangdata.com.cn/Author/Search?AuthorName=%E5%94%90%E9%93%81%E9%92%B0&Version=Professional&ExceptAuthorId=A0010908495'
#     # headers ={
#     #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     #     'Accept-Encoding': 'gzip, deflate',
#     #     'Accept-Language': 'zh-CN,zh;q=0.9',
#     #     'Cache-Control': 'no-cache',
#     #     'Host': 'med.wanfangdata.com.cn',
#     #     'Pragma': 'no-cache',
#     #     'Proxy-Connection': 'keep-alive',
#     #     'Upgrade-Insecure-Requests': '1',
#     #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
#     # }
#     # response = requests.get(url=url,headers=headers)
#     # html = etree.HTML(response.text)
#     # lis = html.xpath("//ul[@id='Professional_all']/li")
#     # name_url = 'http://med.wanfangdata.com.cn/Author/Name'
#     # for li in lis:
#     #     id = li.xpath('./a/text()')[0]
#     #     data = {
#     #         "id":id
#     #     }
#     #     headers_1 = {
#     #         'Accept': '*/*',
#     #         'Accept-Encoding': 'gzip, deflate',
#     #         'Accept-Language': 'zh-CN,zh;q=0.9',
#     #         'Cache-Control': 'no-cache',
#     #         'Content-Length': '13',
#     #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     #         'Host': 'med.wanfangdata.com.cn',
#     #         'Origin': 'http://med.wanfangdata.com.cn',
#     #         'Pragma': 'no-cache',
#     #         'Proxy-Connection': 'keep-alive',
#     #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
#     #     }
#     #     response = requests.post(url=name_url,headers=headers_1,data=data)
#     #     print(response.json())
#     # dic={'name':1}
#     # print(len(dic))
#     html='''
#     <div class="author-list-operation">&#13;
#             <a class="operation-btn udl" href="http://f.med.wanfangdata.com.cn/Fulltext?Id=PeriodicalPaper_aqyjk200604033" target="_blank">&#13;
#                 下载全文&#13;
#             </a>&#13;
#             <a class="operation-btn udl" href="http://f.med.wanfangdata.com.cn/Fulltext?inline=True&amp;id=PeriodicalPaper_aqyjk200604033" target="_blank">&#13;
#                 在线阅读&#13;
#             </a>&#13;
#     </div>&#13;
#     '''
#     html=etree.HTML(html)
#     read_url = html.xpath('//div[@class="author-list-operation"]/a[2]/@href')[0]
#
#     pass
# if __name__ == '__main__':
#     run()
# uuid=md5('http://med.wanfangdata.com.cn/Author/General/A008302840')
# print(uuid)

# def create_subsection():
# a=20
# print(a in range(1,100))
