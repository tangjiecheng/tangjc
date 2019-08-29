import json
import traceback

from config import DB_CONFIG_SPIDER
from dboper_base3 import DbOperBase
from save_author_info import save_author_relative
from tools import start, md5, lxml_to_string

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

def get_url(begin_id,end_id,path):
    try:
        last_ls=get_last(path)
        last_id=last_ls[0]
        last_page=last_ls[1]
        last_index=last_ls[2]

        sql='select id,uuid,name,author_id,author_url,begin_year,end_year from t_cl_author_wanfang_detail where id>={} and id<{}'.format(begin_id,end_id)
        list_ret=DbOperBase.common_select(sql,None,DB_CONFIG_SPIDER,True)
        for item in list_ret:
            id=item['id']
            if id<last_id:
                continue
            author_uuid=item['uuid']
            name=item['name']
            author_id=item['author_id']
            author_url=item['author_url']
            begin_year=item['begin_year']
            end_year=item['end_year']


            parse_next(id,author_uuid,name,author_url,author_id,begin_year,end_year,path,last_page,last_index)
            last_page=1
            last_index = 0
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

# 爬取下一页
def parse_next(id,author_uuid,name,author_url,author_id,begin_years,end_years,path,last_page,last_index):
    url = 'http://med.wanfangdata.com.cn/Author/Statistics?id={}'.format(author_id)
    html = start(url)
    try:
        if len(html.xpath('//li[@class="hidden-sm"]/span/text()'))!=0:
            total_page=html.xpath('//li[@class="hidden-sm"]/span/text()')[0].strip('共页')
            for page in range(1,int(total_page)+1):
                if page<last_page:
                    continue
                url='http://med.wanfangdata.com.cn/Author/StatisticsPaperList?P={}&Id={}&QueryCode=000&BeginYear={}&EndYear={}&Keywords='.format(str(page),author_id,begin_years,end_years)
                html=start(url)
                parse_literature_info(id,author_uuid,name,author_url,author_id,url,html,page,path,last_index)
                last_index = 0
        else:
            page=1
            parse_literature_info(id,author_uuid,name,author_url,author_id,url,html,page,path,last_index)
            last_index = 0
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

# 爬取论文信息
def parse_literature_info(id,author_uuid,author_name,author_url,author_id,source_url,html,page,path,last_index):
    try:
        html_str=lxml_to_string(html)
        literature_ls=html.xpath('//ul[@class="author-list"]/li')
        literature_index=1
        for item in literature_ls:
            if literature_index<=last_index:
                literature_index+=1
                continue
            source_text=lxml_to_string(item)
            if len(item.xpath('./div[@class="author-list-title"]/span[@class="title-only"]/text()'))!=0:
                label=item.xpath('./div[@class="author-list-title"]/span[@class="title-only"]/text()')[0]
            else:label=''
            num=item.xpath('./div[@class="author-list-title"]/span[@class="num"]/text()')[0].strip('.')
            title=item.xpath('./div[@class="author-list-title"]/a/text()')[0]
            url=item.xpath('./div[@class="author-list-title"]/a/@href')[0]
            uuid=md5(url)
            periodical_type=item.xpath('./div[@class="author-list-type"]/b/text()')[0]
            author_ls=item.xpath('./div[@class="author-list-type"]/a')
            ls=[]
            for author_item in author_ls:
                author_dic={}
                a_url=author_item.xpath('./@href')[0]
                name=author_item.xpath('./text()')[0]
                uuid=md5(a_url)
                author_id=a_url.split('/')[-1]
                author_dic['uuid']=uuid
                author_dic['name']=name
                author_dic['author_id']=author_id
                author_dic['url']=a_url
                ls.append(author_dic)
            author_info=json.dumps(ls,ensure_ascii=False)
            # 所在期刊
            periodical=item.xpath('./div[@class="author-list-type-info"]/a[1]/text()')[0]
            periodical_url=item.xpath('./div[@class="author-list-type-info"]/a[1]/@href')[0]
            periodical_uuid=md5(periodical_url)
            # 期数链接链接
            period_url = item.xpath('./div[@class="author-list-type-info"]/a[2]/@href')[0]
            # 期数
            period=item.xpath('./div[@class="author-list-type-info"]/a[2]/text()')[0]
            # 期数链接
            period_url = item.xpath('./div[@class="author-list-type-info"]/a[2]/@href')[0]
            # 页码
            pagination=item.xpath('./div[@class="author-list-type-info"]/a[2]/following::text()')[0].strip()
            # 被引数
            cite_num=item.xpath('./div[@class="author-list-type-info"]/span[1]/text()')[0].strip()
            # 收录信息
            include_info_ls=item.xpath('./div[@class="author-list-type-info"]/span[@class="core-img"]')
            ls=[]
            if len(include_info_ls)!=0:
                for include_item in include_info_ls:
                    include_dic={}
                    include_name=include_item.xpath('./text()')[0]
                    detail=include_item.xpath('./@title')[0]
                    include_dic['name']=include_name
                    include_dic['detail']=detail
                    ls.append(include_dic)
                include_info=json.dumps(ls,ensure_ascii=False)
            else:include_info=None
            # 摘要
            intro = '<'+lxml_to_string(item.xpath('./div[@class="author-list-main"]')[0]).replace('&#13;','').replace('\n','').strip('<div class="author-list-main"></div>')
            # intro='<'+item.xpath('./div[@class="author-list-main"]/string(.)')[0]
            #关键词
            keywords_ls=item.xpath('./div[@class="author-list-keyword"]/a')
            if len(keywords_ls)!=0:
                ls=[]
                for keywords_item in keywords_ls:
                    keyword_dic={}
                    k_url = keywords_item.xpath('./@href')[0]
                    try:
                        keyword=keywords_item.xpath('./text()')[0]
                    except:
                        keyword=k_url.split('=')[-1].strip('()')
                    keyword_dic['keyword']=keyword
                    keyword_dic['url']=k_url
                    ls.append(keyword_dic)
                keywords=json.dumps(ls,ensure_ascii=False)
            else:keywords=None
            # str_test=lxml_to_string(item.xpath('.//div[@class="author-list-operation"]')[0])
            #在线阅读链接
            read_url=''
            if len(item.xpath('.//div[@class="author-list-operation"]/a[2]/@href'))!=0:
                read_url=item.xpath('.//div[@class="author-list-operation"]/a[2]/@href')[0]
            #下载链接
            download_url=''
            if len(item.xpath('.//div[@class="author-list-operation"]/a[1]/@href'))!=0:
                download_url=item.xpath('.//div[@class="author-list-operation"]/a[1]/@href')[0]
            pass


            save_author_relative(id, uuid, source_url, source_text, author_uuid, author_id, author_url,
                                 author_name, num,title, url, label, periodical_type, author_info, periodical,
                                 periodical_url, period_url,period, pagination, cite_num, include_info, intro, keywords, read_url,
                                 download_url
                                 )

            record_last(id, page, literature_index, path)
            literature_index+=1


    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

# 记录断点
def record_last(id,page,literature_index,path):
    with open(path,'w',encoding='utf-8') as f:
        r_ls=[id,page,literature_index]
        r_json=json.dumps(r_ls,ensure_ascii=False)
        f.write(r_json)
# 读取断点
def get_last(path):
    with open(path,'r',encoding='utf-8') as f:
        last_json=f.read()
        last_ls=json.loads(last_json)
        return last_ls

if __name__ == '__main__':
    # author_id='A000011181'
    # html=start('http://med.wanfangdata.com.cn/Author/Statistics?id=A000011181')
    # begin_years='1998'
    # end_years='2019'
    # parse_next(author_id,html,begin_years,end_years)
    path='relative_last/last01.txt'
    get_url(133,1000,path)