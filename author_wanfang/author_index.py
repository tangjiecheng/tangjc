import json
import traceback

from config import DB_CONFIG_SPIDER
from dboper_base3 import DbOperBase
from same_name_author import get_next_url
from save_author_info import save_author_index
from tools import start

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

'''
obj_type
1--期刊
2--文献
3--指南
4--文献相关作者
5--指南相关作者
6--同名作者
7--相关合作作者
'''


def get_index_author(begin_id,end_id):
    try:
        sql='SELECT id,uuid,`name`,author_id,author_url,obj_uuid,obj_type,obj_name,obj_url FROM t_cl_author_wanfang WHERE id>={} AND id<{} AND (obj_type="期刊" OR obj_type="文献" OR obj_type="指南") AND uuid is not null and UUID NOT IN (SELECT UUID FROM t_cl_author_wanfang_index)'.format(begin_id,end_id)
        list_ret = DbOperBase.common_select(sql, None, DB_CONFIG_SPIDER, True)
        for item in list_ret:
            source_id=item['id']
            uuid=item['uuid']
            name=item['name']
            author_id=item['author_id']
            author_url=item['author_url']
            obj_uuid=item['obj_uuid']
            obj_type=deal_obj_type(item['obj_type'])
            obj_name=item['obj_name']
            obj_url=item['obj_url']
            # list_index=[uuid,name,author_id,obj_uuid,obj_type,obj_name,obj_url]
            save_author_index(source_id,uuid,name,author_id,author_url,obj_uuid,obj_type,obj_name,obj_url)
            pass
    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def deal_obj_type(type):
    obj_type=2
    if type=='期刊':
        obj_type=1
    if type=='文献':
        obj_type=2
    if type=='机构':
        obj_type=3
    return obj_type

def get_index_literature(begin_id,end_id):
    try:
        sql='select id,uuid,title,paper_url,relevant_author from t_cl_literature_medicine_wanfang_detail where id>={} and id<{} and relevant_author is not null and relevant_author!="[]"'.format(begin_id,end_id)
        list_ret = DbOperBase.common_select(sql, None, DB_CONFIG_SPIDER, True)
        for item in list_ret:
            source_id=item['id']
            relevant_author=item['relevant_author']

            obj_uuid=item['uuid']
            obj_url=item['paper_url']
            obj_type=4
            obj_name=item['title']

            path='literature.txt'
            record_last(source_id,path)

            relevant_author_ls=json.loads(relevant_author)
            for author_item in relevant_author_ls:
                uuid=author_item['uuid']
                author_id=author_item['author_id']
                name=author_item['author_name']
                author_url=author_item['author_url']
                save_author_index(source_id, uuid, name, author_id, author_url, obj_uuid, obj_type, obj_name, obj_url)
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass


def get_index_guide(begin_id, end_id):
    try:
        sql = 'select id,uuid,title,paper_url,relevant_author from t_cl_guide_clinical_wanfang_detail where id>={} and id<{} and relevant_author is not null and relevant_author!="[]"'.format(
            begin_id, end_id)
        list_ret = DbOperBase.common_select(sql, None, DB_CONFIG_SPIDER, True)
        for item in list_ret:
            source_id = item['id']
            relevant_author = item['relevant_author']

            obj_uuid = item['uuid']
            obj_url = item['paper_url']
            obj_type = 5
            obj_name = item['title']

            path = 'guide.txt'
            record_last(source_id, path)

            relevant_author_ls = json.loads(relevant_author)
            for author_item in relevant_author_ls:
                uuid = author_item['uuid']
                author_id = author_item['author_id']
                name = author_item['author_name']
                author_url = author_item['author_url']
                save_author_index(source_id, uuid, name, author_id, author_url, obj_uuid, obj_type, obj_name, obj_url)
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass

def get_index_same_author(begin_id,end_id):
    try:
        sql='select id,author_id,name from t_cl_author_wanfang_index where obj_type!=6'
        list_ret=DbOperBase.common_select(sql,None,DB_CONFIG_SPIDER,True)
        for item in list_ret:
            id=item['id']
            author_id=item['author_id']
            name=item['name']
            url='http://med.wanfangdata.com.cn/Author/Search?AuthorName={}&Version=Professional&ExceptAuthorId={}'.format(name,author_id)
            html=start(url)
            get_next_url()
    except Exception as x:
        err = traceback.format_exc()
        print(err)
        pass

def record_last(id,path):
    with open(path,'w',encoding='utf-8') as f:
        f.write(str(id))

if __name__ == '__main__':
    # begin_id=70000
    while True:
        # end_id=begin_id+10000
        get_index_author(begin_id,end_id)
        # begin_id=end_id
    # get_index_literature(1,1000)
    # get_index_guide(1,1000)

        # 5317873

