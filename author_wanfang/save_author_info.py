import time
import traceback

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')

from config import DB_CONFIG_SPIDER
from dboper_base3 import DbOperBase, SqlCreate


def save_author_index(source_id,uuid,name,author_id,author_url,obj_uuid,obj_type,obj_name,obj_url):
    dboper = DbOperBase()
    dboper.set_cfg(DB_CONFIG_SPIDER)
    dboper.open_db_conn()
    dboper.trans_begin()
    try:
        create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('正在插入--' + str(source_id) + ' ' + name + ' ' + create_time)
        sql_create = SqlCreate()
        # sql_create.add_insert_param('source_id', source_id)

        sql_create.add_insert_param('uuid', uuid)
        sql_create.add_insert_param('name', name)
        sql_create.add_insert_param('author_id', author_id)
        sql_create.add_insert_param('author_url', author_url)

        sql_create.add_insert_param('obj_uuid', obj_uuid)
        sql_create.add_insert_param('obj_type', obj_type)
        sql_create.add_insert_param('obj_name', obj_name)
        sql_create.add_insert_param('obj_url', obj_url)

        sql_create.add_insert_param('create_time', create_time)


        sql = sql_create.generate_insert_sql('t_cl_author_wanfang_index')
        dboper.execute(sql)
        last_row_id = dboper.last_rowid()
        dboper.trans_commit()
        print('插入成功')
        print('*****************************')
    except Exception as x:
        print('插入失败')
        err=traceback.format_exc()
        print(err)
        print('*****************************')
        pass
    finally:
        dboper.close_db_conn()


def save_author_detail(source_id,uuid,source_url,source_text,author_id,name,author_url,obj_uuid,obj_type,obj_name,obj_url,SameName_author,
                       pub_author_all,pub_author_first,click_author,org,org_url,cooperation_relation_org,cooperation_relation_author,
                       cooperation_author,periodical,fund,relative_keywords,pub_statistics,begin_year,end_year
                       ):
    dboper = DbOperBase()
    dboper.set_cfg(DB_CONFIG_SPIDER)
    dboper.open_db_conn()
    dboper.trans_begin()
    try:
        create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('正在插入--' + str(source_id) + ' ' + name + ' ' + create_time)
        sql_create = SqlCreate()
        sql_create.add_insert_param('source_id', source_id)

        sql_create.add_insert_param('source_url', source_url)
        sql_create.add_insert_param('source_text', source_text)

        sql_create.add_insert_param('uuid', uuid)
        sql_create.add_insert_param('name', name)
        sql_create.add_insert_param('author_id', author_id)
        sql_create.add_insert_param('author_url', author_url)

        sql_create.add_insert_param('obj_uuid', obj_uuid)
        sql_create.add_insert_param('obj_type', obj_type)
        sql_create.add_insert_param('obj_name', obj_name)
        sql_create.add_insert_param('obj_url', obj_url)

        sql_create.add_insert_param('SameName_author', SameName_author)
        sql_create.add_insert_param('pub_author_all', pub_author_all)
        sql_create.add_insert_param('pub_author_first', pub_author_first)
        sql_create.add_insert_param('click_author', click_author)

        sql_create.add_insert_param('org', org)
        sql_create.add_insert_param('org_url', org_url)
        sql_create.add_insert_param('cooperation_relation_org', cooperation_relation_org)
        sql_create.add_insert_param('cooperation_relation_author', cooperation_relation_author)
        sql_create.add_insert_param('cooperation_author', cooperation_author)


        sql_create.add_insert_param('periodical', periodical)
        sql_create.add_insert_param('fund', fund)
        sql_create.add_insert_param('relative_keywords', relative_keywords)
        sql_create.add_insert_param('pub_statistics', pub_statistics)

        sql_create.add_insert_param('begin_year', begin_year)
        sql_create.add_insert_param('end_year', end_year)

        sql_create.add_insert_param('create_time', create_time)


        sql = sql_create.generate_insert_sql('t_cl_author_wanfang_detail')
        dboper.execute(sql)
        last_row_id = dboper.last_rowid()
        dboper.trans_commit()
        print('插入成功')
        print('*****************************')
    except Exception as x:
        print('插入失败')
        err=traceback.format_exc()
        print(err)
        print('*****************************')
        pass
    finally:
        dboper.close_db_conn()


def save_author_relative(source_id, uuid, source_url, source_text, author_uuid, author_id, author_url,
                                 author_name, num,title, url, label, periodical_type, author_info, periodical,
                                 periodical_url, period_url,period, pagination, cite_num, include_info, intro,
                                keywords, read_url,download_url
                         ):
    dboper = DbOperBase()
    dboper.set_cfg(DB_CONFIG_SPIDER)
    dboper.open_db_conn()
    dboper.trans_begin()
    try:
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('正在插入--' + str(source_id) + ' ' + author_name + '--' +title+' '+ create_time)
        print(source_url)
        sql_create = SqlCreate()
        sql_create.add_insert_param('uuid', uuid)
        sql_create.add_insert_param('source_url', source_url)
        sql_create.add_insert_param('source_text', source_text)
        sql_create.add_insert_param('author_id', author_id)
        sql_create.add_insert_param('author_url', author_url)
        sql_create.add_insert_param('author_name', author_name)
        sql_create.add_insert_param('author_uuid', author_uuid)

        sql_create.add_insert_param('num', num)
        sql_create.add_insert_param('title', title)
        sql_create.add_insert_param('url', url)
        sql_create.add_insert_param('label', label)
        sql_create.add_insert_param('periodical_type', periodical_type)
        sql_create.add_insert_param('author_info', author_info)

        sql_create.add_insert_param('periodical', periodical)
        sql_create.add_insert_param('periodical_url', periodical_url)
        sql_create.add_insert_param('period', period)
        sql_create.add_insert_param('period_url', period_url)
        sql_create.add_insert_param('pagination', pagination)
        sql_create.add_insert_param('cite_num', cite_num)
        sql_create.add_insert_param('include_info', include_info)
        sql_create.add_insert_param('intro', intro)
        sql_create.add_insert_param('keywords', keywords)
        sql_create.add_insert_param('read_url', read_url)
        sql_create.add_insert_param('download_url', download_url)

        sql_create.add_insert_param('create_time', create_time)

        sql = sql_create.generate_insert_sql('t_cl_author_wanfang_relative')
        dboper.execute(sql)
        last_row_id = dboper.last_rowid()
        dboper.trans_commit()
        print('插入成功')
        print('*****************************')
    except Exception as x:
        print('插入失败')
        err=traceback.format_exc()
        print(err)
        print('*****************************')
        pass
    finally:
        dboper.close_db_conn()
