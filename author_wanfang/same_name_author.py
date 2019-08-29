import json
import traceback

import requests

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

from author_tools import is_page_false
from headers_wanfang import ranking_list_headers
from save_author_info import save_author_index
from tools import start, md5, lxml_to_string

domain='http://med.wanfangdata.com.cn'
def get_url(id,author_id,url,obj_type):
    try:
        # SameName_author=None
        html=start(url)
        page_status=is_page_false(html)
        if page_status:
            source_text=lxml_to_string(html)
            pub_author_all=parse_all_pub_num(html)
            pub_author_first=parse_first_pub_num(html)
            click_author=parse_click_num(html)
            SameName_author = get_next_url(id,author_id,url,html,obj_type)
            return [SameName_author, pub_author_all, pub_author_first, click_author, source_text]
        else:
            return [None, None, None, None, None]


    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass

def get_url_other(url):
    try:
        html=start(url)
        pub_author_all=parse_all_pub_num(html)
        pub_author_first=parse_first_pub_num(html)
        click_author=parse_click_num(html)
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass

def get_next_url(id,author_id,url,html,obj_type):
    try:
        page_num=1
        ls=[]
        while True:
            print(page_num)
            # parse_same_name_author(html)
            SameName_author_part = parse_same_name_author(id,author_id,url,html,obj_type)
            ls.append(SameName_author_part)
            SameName_author = json.dumps(ls, ensure_ascii=False)
            if SameName_author=='[null]':
                SameName_author=None
            if len(html.xpath('//li[@class="next"]/a'))!=0:
                next_url=domain+html.xpath('//li[@class="next"]/a/@href')[0]
                html=start(next_url)
                page_num+=1
            else:
                return SameName_author
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass


def parse_same_name_author(id,author_id,url,html,obj_type):
    try:
        author_list=html.xpath('//ul[@class="author-list"]/li')
        if len(author_list)!=0:
            ls=[]
            for item in author_list:
                dic={}
                same_author_name = item.xpath('./div[@class="author-list-title"]/a/text()')[0]
                same_author_url=domain+item.xpath('./div[@class="author-list-title"]/a/@href')[0].replace('Professional','General')
                same_author_id=same_author_url.split('/')[-1]
                same_author_org=item.xpath('./div[@class="author-list-content"]/span[1]/text()')[0].split('：')[-1]
                same_author_pub_num=item.xpath('./div[@class="author-list-content"]/span[2]/text()')[0].split('：')[-1]
                uuid=md5(same_author_url)
                dic['uuid']=uuid
                dic['author_id']=same_author_id
                dic['name']=same_author_name
                dic['url']=same_author_url
                dic['org']=same_author_org
                dic['pun_num']=same_author_pub_num

                if obj_type!=6 and obj_type!=7:
                    # same_obj_uuid = ''
                    # same_obj_type = 6
                    # same_obj_name = ''
                    # same_obj_url = ''
                    save_author_index(source_id=id,uuid=uuid,name=same_author_name,author_id=same_author_id,author_url=same_author_url,obj_uuid=md5(url),obj_type=6,obj_name=author_id,obj_url=url)
                ls.append(dic)
            SameName_author=json.dumps(ls,ensure_ascii=False)
        else:SameName_author=None
        return SameName_author

    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass
def parse_all_pub_num(html):
    try:
        all_pub_num_list=html.xpath('//ul[@id="Professional_all"]/li')
        ls=[]
        for item in all_pub_num_list:
            dic={}
            url=domain+item.xpath('./a/@href')[0]
            author_id=item.xpath('./a/@authorid')[0]
            name = get_name(author_id)
            pub_num=item.xpath('./span/text()')[0]
            uuid=md5(domain)
            dic['uuid']=uuid
            dic['author_id']=author_id
            dic['name']=name
            dic['url']=url
            dic['pub_num']=pub_num
            ls.append(dic)
        pub_author_all=json.dumps(ls,ensure_ascii=False)
        return pub_author_all
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass
def parse_first_pub_num(html):
    try:
        firs_pub_num_list=html.xpath('//ul[@id="Professional_first"]/li')
        ls=[]
        for item in firs_pub_num_list:
            dic={}
            url=domain+item.xpath('./a/@href')[0]
            author_id=item.xpath('./a/@authorid')[0]
            pub_num=item.xpath('./span/text()')[0]
            name = get_name(author_id)
            uuid=md5(url)
            dic['uuid'] = uuid
            dic['author_id'] = author_id
            dic['name'] = name
            dic['url'] = url
            dic['pub_num'] = pub_num
            ls.append(dic)
        pub_author_first = json.dumps(ls, ensure_ascii=False)
        return pub_author_first

    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass
def parse_click_num(html):
    try:
        click_num_list = html.xpath('//ul[@class="nlst3 clear"]/li')
        ls=[]
        for item in click_num_list:
            dic={}
            url = domain+item.xpath('./a/@href')[0]
            uuid=md5(url)
            author_id = item.xpath('./a/@authorid')[0]
            author_id=url.split('/')[-1].strip('?version=Professional')
            name = get_name(author_id)
            pub_num = item.xpath('./span/text()')[0]
            dic['uuid'] = uuid
            dic['author_id'] = author_id
            dic['name'] = name
            dic['url'] = url
            dic['pub_num'] = pub_num
            ls.append(dic)
        click_author = json.dumps(ls, ensure_ascii=False)
        return click_author
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def get_name(author_id):
    FormData={
        'id':author_id
    }
    # data=parse.urlencode(FormData)
    url='http://med.wanfangdata.com.cn/Author/Name'
    try:
        response=requests.post(url,FormData,headers=ranking_list_headers()).text
        return response
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass





# if __name__ == '__main__':
#     url = 'http://med.wanfangdata.com.cn/Author/Search?AuthorName=%E5%BC%A0%E7%8E%89%E6%A2%85&Version=Professional&ExceptAuthorId=A000011181'
#     get_url(url)
