import json
import traceback

import author_base_info
import author_statistics_info
import same_name_author
from config import DB_CONFIG_SPIDER
from dboper_base3 import DbOperBase
from save_author_info import save_author_detail

import sys
sys.path.append('F:\python\project\author_wanfang\author_relative_spiders')


def get_url(begin_id,end_id,path):
    try:
        last_id=get_last(path)

        # begin_id=last_id+1
        while begin_id<end_id:
            if begin_id<last_id:
                begin_id+=1
                continue
            sql='select id,uuid,author_url,obj_name,obj_uuid,obj_url,obj_type,author_id,name from t_cl_author_wanfang_index where id={}'.format(begin_id)
            list_ret=DbOperBase.common_select(sql,None,DB_CONFIG_SPIDER,True)
            # for item in list_ret:
                # id=item['id']
                # uuid=item['uuid']
                # author_url=item['author_url']
                # obj_name=item['obj_name']
                # obj_uuid=item['obj_uuid']
                # obj_type=item['obj_type']
                # obj_url=item['obj_url']
                # author_id=item['author_id']
                # name=item['name']

            id = list_ret[0]['id']
            uuid = list_ret[0]['uuid']
            author_url = list_ret[0]['author_url']
            obj_name = list_ret[0]['obj_name']
            obj_uuid = list_ret[0]['obj_uuid']
            obj_type = list_ret[0]['obj_type']
            obj_url = list_ret[0]['obj_url']
            author_id = list_ret[0]['author_id']
            name = list_ret[0]['name']
            same_url='http://med.wanfangdata.com.cn/Author/Search?AuthorName={}&Version=Professional&ExceptAuthorId={}'.format(name,author_id)
            same_ls=same_name_author.get_url(id,author_id,same_url,obj_type)

            base_url='http://med.wanfangdata.com.cn/Author/Professional/{}'.format(author_id)
            base_ls=author_base_info.get_url(id,base_url,author_id,obj_type)

            statistics_url='http://med.wanfangdata.com.cn/Author/Statistics?id={}'.format(author_id)
            statistics_ls=author_statistics_info.get_url(author_id,statistics_url)

            SameName_author=same_ls[0]
            pub_author_all=same_ls[1]
            pub_author_first=same_ls[2]
            click_author=same_ls[3]
            source_text_same=same_ls[4]

            # [author_org_ls[0], author_org_ls[1], cooperation_relation_org, cooperation_relation_author,cooperation_author, source_text]
            org=base_ls[0]
            org_url=base_ls[1]
            cooperation_relation_org=base_ls[2]
            cooperation_relation_author=base_ls[3]
            cooperation_author=base_ls[4]
            source_text_base=base_ls[5]

            # [periodical, fund, relative_keywords, s_ls[0], s_ls[1], s_ls[2], source_text]
            periodical=statistics_ls[0]
            fund=statistics_ls[1]
            relative_keywords=statistics_ls[2]
            pub_statistics=statistics_ls[3]
            begin_year=statistics_ls[4]
            end_year=statistics_ls[5]
            source_text_statistics=statistics_ls[6]

            source_url_ls=[same_url,base_url,statistics_url]
            source_url=json.dumps(source_url_ls,ensure_ascii=False)

            source_text_ls=[source_text_same,source_text_base,source_text_statistics]
            source_text=json.dumps(source_text_ls,ensure_ascii=False)

            save_author_detail(id, uuid, source_url, source_text, author_id, name, author_url, obj_uuid,
                               obj_type, obj_name, obj_url, SameName_author,
                               pub_author_all, pub_author_first, click_author, org, org_url, cooperation_relation_org,
                               cooperation_relation_author,
                               cooperation_author, periodical, fund, relative_keywords, pub_statistics, begin_year,
                               end_year
                               )

            record_last(id,path)
            begin_id+=1


    except Exception as x:
        err=traceback.format_exc()
        print(err)
        pass

def record_last(id,path):
    with open(path,'w',encoding='utf-8') as f:
        f.write(str(id))
def get_last(path):
    with open(path,'r',encoding='utf-8') as f:
        last_id=f.read()
        return int(last_id)

# if __name__ == '__main__':
#     get_url(1,1000)