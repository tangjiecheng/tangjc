import json
import traceback

import requests

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

from author_tools import is_page_false
from headers_wanfang import base_info_headers
from save_author_info import save_author_index
from tools import start, md5, lxml_to_string

domain='http://med.wanfangdata.com.cn'
def get_url(id,url,author_id,obj_type):
    try:
        html=start(url)
        page_statuse=is_page_false(html)
        if page_statuse:
            source_text=lxml_to_string(html)
            author_org_ls=parse_author_info(html)
            cooperation_author=parse_author_cooperation(id,url,author_id,html,obj_type)
            cooperation_relation_org=parse_org_cooperation(html)
            cooperation_relation_author=parse_author_cooperation_relation(author_id)
            return [author_org_ls[0],author_org_ls[1],cooperation_relation_org,cooperation_relation_author,cooperation_author,source_text]
        else:
            return ['','',None,None,None,None]
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def parse_author_info(html):
    try:
        name=html.xpath('//div[@class="author-info clear"]/div[@class="author-info-item clear"]/span[1]/text()')[0]
        author_id=html.xpath('//div[@class="author-info clear"]/div[@class="author-info-item clear"]/span[2]/text()')[0].strip('ID:')
        author_org=html.xpath('//div[@class="author-info clear"]/div[@class="author-info-item"][1]/a/@title')[0]
        author_org_url=html.xpath('//div[@class="author-info clear"]/div[@class="author-info-item"][1]/a/@href')[0]
        return [author_org,author_org_url]

    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass
def parse_org_cooperation(html):
    try:
        org_ls=html.xpath('//ul[@class="nlst3"]/li')
        if len(org_ls)!=0:
            ls=[]
            for item in org_ls:
                dic={}
                url=item.xpath('./a/@href')[0]
                org=item.xpath('./a/@title')[0]
                cooperationTimes=item.xpath('./span/text()')[0]
                dic['org']=org
                dic['url']=url
                dic['cooperationTimes']=cooperationTimes
                ls.append(dic)
            cooperation_relation_org=json.dumps(ls,ensure_ascii=False)
        else:cooperation_relation_org=None
        return cooperation_relation_org


    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def parse_author_cooperation(id,url,author_id,html,obj_type):
    try:
        author_ls=html.xpath('//div[@class="tag-content"]/span[@class="lnk2"]')
        if len(author_ls)!=0:
            ls=[]
            for item in author_ls:
                dic={}
                name=item.xpath('./a/text()')[0]
                url=domain+item.xpath('./a/@href')[0].replace('Professional','General')
                author_id=url.split('/')[-1]
                uuid=md5(url)
                dic['uuid']=uuid
                dic['author_id']=author_id
                dic['name']=name
                dic['url']=url


                # obj_uuid = ''
                # obj_type = 7
                # obj_name = ''
                # obj_url = ''
                if obj_type !=6 and obj_type!=7:
                    save_author_index(source_id=id,uuid=uuid,name=name,author_id=author_id,author_url=url,obj_uuid=md5(url),obj_type=7,obj_name=author_id,obj_url=url)
                ls.append(dic)
            cooperation_author=json.dumps(ls,ensure_ascii=False)
        else:cooperation_author=None
        return cooperation_author
        pass
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def parse_author_cooperation_relation(author_id):
    data=get_RelationChartData(author_id)
    try:
        data_dic=json.loads(data)
    except:
        data_dic={}
    author_cooperation_ls=[]
    cooperation_relation_ls=[]
    if len(data_dic)!=0:
        for item1 in data_dic['links']:
            dic={}
            for item2 in data_dic['nodes']:
                if item1['source']==item2['index']:
                    source_name = item2['name']
                    source_author_id = item2['id']
                    source_url = 'http://med.wanfangdata.com.cn/Author/Professional/' + source_author_id
                    source_uuid=md5(source_url)
                    cooperationTimes = item1['cooperationTimes']


                    dic['source_name'] = source_name
                    dic['source_author_id'] = source_author_id
                    dic['source_url'] = source_url
                    dic['source_uuid'] = source_uuid
                    dic['cooperationTimes']=cooperationTimes
                    continue
                if item1['target']==item2['index']:
                    target_name=item2['name']
                    target_author_id = item2['id']
                    target_url = 'http://med.wanfangdata.com.cn/Author/Professional/' + target_author_id
                    target_uuid = md5(target_url)

                    dic['target_name'] = target_name
                    dic['target_author_id'] = target_author_id
                    dic['target_url'] = target_url
                    dic['target_uuid'] = target_uuid
                    continue
            cooperation_relation_ls.append(dic)
        cooperation_relation_author=json.dumps(cooperation_relation_ls,ensure_ascii=False)
    else:cooperation_relation_author=None
    return cooperation_relation_author


    # for item1 in data_dic['links']:
    #     dic1={}
    #     source=['source']
    #     target=['target']
    #     cooperationTimes=item1['cooperationTimes']
    #     dic
    #
    #
    #
    # for item2 in data_dic['nodes']:
    #     dic={}
    #     name=item2['name']
    #     author_id=item2['id']
    #     index=item2['index']
    #     url='http://med.wanfangdata.com.cn/Author/Professional/'+author_id
    #     uuid=md5(url)
    #     dic['uuid']=uuid
    #     dic['author_id']=author_id
    #     dic['name']=name
    #     dic['url']=url
    #     author_cooperation_ls.append(dic)
    pass

def get_RelationChartData(author_id):
    url='http://med.wanfangdata.com.cn/Author/RelationChartData'
    try:
        FormData={
            'id':author_id
        }

        # data='id:{}'.format(author_id)
        headers=base_info_headers()
        # data=parse.urlencode(FormData)
        response=requests.post(url=url,data=FormData,headers=base_info_headers()).text
        return response
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass
if __name__ == '__main__':
    url='http://med.wanfangdata.com.cn/Author/Professional/A000011181'
    get_url(url)