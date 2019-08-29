import json
import traceback

import requests

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

from author_tools import is_page_false
from tools import start, lxml_to_string

domain = 'http://med.wanfangdata.com.cn'


def get_url(author_id,url):
    try:
        html = start(url)
        page_status=is_page_false(html)
        if page_status:
            source_text=lxml_to_string(html)
            periodical=parse_pub_perio(html)
            fund=parse_fund_relation(html)
            relative_keywords=parse_relative_keywords(html)
            s_ls=parse_analysis_url(author_id,html)
            return [periodical,fund,relative_keywords,s_ls[0],s_ls[1],s_ls[2],source_text]
        else:
            return [None, None, None, None, None, None, None]
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass


def parse_pub_perio(html):
    try:
        perio_ls = html.xpath('//ul[@class="nlst3"][1]/li')
        ls=[]
        for item in perio_ls:
            dic={}
            name = item.xpath('./a/@title')[0]
            url = domain + item.xpath('./a/@href')[0]
            num = item.xpath('./span/text()')[0]
            dic['name']=name
            dic['url']=url
            dic['num']=num
            ls.append(dic)
        periodical=json.dumps(ls,ensure_ascii=False)
        return periodical
        pass
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass


def parse_fund_relation(html):
    try:
        # fund_ls=html.xpath('//ul[@class="nlst3"]')
        fund_ls = html.xpath('//ul[@class="nlst3"][2]/li')
        ls=[]
        if len(fund_ls) != 0:
            for item in fund_ls:
                dic={}
                name = item.xpath('./a/@title')[0]
                url = domain + item.xpath('./a/@href')[0]
                num = item.xpath('./span/text()')[0]
                dic['name']=name
                dic['url']=url
                dic['num']=num
                ls.append(dic)
            fund=json.dumps(ls,ensure_ascii=False)

            pass
        else:fund=None
        return fund
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass


def parse_relative_keywords(html):
    try:
        keywords_ls = html.xpath('//div[@class="tag-content"]/span')
        if len(keywords_ls)!=0:
            relative_keywords_ls=[]
            for item in keywords_ls:
                dic={}
                keyword=item.xpath('./a/@title')[0]
                url=domain+item.xpath('./a/@href')[0]
                dic['keyword']=keyword
                dic['url']=url
                relative_keywords_ls.append(dic)
            relative_keywords=json.dumps(relative_keywords_ls,ensure_ascii=False)
        else:relative_keywords=None
        return relative_keywords
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass

def parse_analysis_url(author_id,html):
    try:
        begin_year=html.xpath('//select[@id="beginYear"]/option[1]/text()')[0]
        end_year=html.xpath('//select[@id="beginYear"]/option[last()]/text()')[0]
        query_code_ls=['100','101','110','111','000','001','010','011']
        ls=[]
        for query_code in query_code_ls:
            limit_ls=deal_query_code(query_code)
            url='http://med.wanfangdata.com.cn/Author/Statistics?Id={}&QueryCode={}&BeginYear={}&EndYear={}'.format(author_id,query_code,begin_year,end_year)
            html=start(url)
            k_ls=parse_analysis(author_id,limit_ls,html,begin_year,end_year,query_code)
            dic={}
            dic['source']=limit_ls[0]
            dic['author_limit']=limit_ls[1]
            dic['periodical_limit']=limit_ls[2]
            dic['year_limit']=begin_year+'-'+end_year
            dic['keywords']=k_ls
            ls.append(dic)
        pub_statistics=json.dumps(ls,ensure_ascii=False)
        return [pub_statistics,begin_year,end_year]

    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass


def parse_analysis(author_id,limit_ls,html,begin_year,end_year,query_code):
    try:
        url='http://med.wanfangdata.com.cn/Author/GetChartData'
        keywords_ls=html.xpath('//ul[@class="trend-chart-word-content"]/li')
        keywords_ls.append('')
        ls=[]
        for item in keywords_ls:
            if item=='':
                keyword=''
            else:
                item_str=lxml_to_string(item)
                keyword=item.xpath('./label/@for')[0]

            data={
                'Id': author_id,
                'QueryCode': query_code,
                'BeginYear': begin_year,
                'EndYear': end_year,
                'Keywords':keyword
            }
            try:
                response=requests.post(url,data).text
                keywords_info_ls=json.loads(response)
                label = keywords_info_ls[0]['label']
                data = keywords_info_ls[0]['data']
            except:
                label = keyword
                data = None
            dic = {}
            dic['label'] = label
            dic['data'] = data
            ls.append(dic)

        return ls

        pass


    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass


def deal_query_code(query_code):
    if query_code == '100':
        source = '中国科技论文统计源期刊资源'
        author_limit='不限'
        periodical_limit='不限'
    if query_code == '101':
        source = '中国科技论文统计源期刊资源'
        author_limit = '不限'
        periodical_limit = '核心期刊'
    if query_code=='110':
        source = '中国科技论文统计源期刊资源'
        author_limit = '第一作者'
        periodical_limit = '不限'
    if query_code=='111':
        source = '中国科技论文统计源期刊资源'
        author_limit = '第一作者'
        periodical_limit = '核心期刊'
    if query_code=='000':
        source = '万方数据收录期刊资源'
        author_limit = '不限'
        periodical_limit = '不限'
    if query_code=='001':
        source = '万方数据收录期刊资源'
        author_limit = '不限'
        periodical_limit = '核心期刊'
    if query_code=='010':
        source = '万方数据收录期刊资源'
        author_limit = '第一作者'
        periodical_limit = '不限'
    if query_code=='011':
        source = '万方数据收录期刊资源'
        author_limit = '第一作者'
        periodical_limit = '核心期刊'
    return [source,author_limit,periodical_limit]

#
# if __name__ == '__main__':
#     url = 'http://med.wanfangdata.com.cn/Author/Statistics?id=A000011181'
#     author_id='A000011181'
#     get_url(author_id,url)
