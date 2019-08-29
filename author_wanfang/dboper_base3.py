#-*-coding:utf-8-*-
__author__ = 'Alex'

import sys
import MySQLdb
import time
import traceback
import datetime

try:
    from sshtunnel import SSHTunnelForwarder
except Exception as x:
    pass

class DbConfig(object):
    def __init__(self,str_host = '',u_port = 0,str_user = '',str_pwd = '',str_db_name = '',str_ssh_domain='',str_ssh_user='',str_ssh_pwd=''):
        self.str_host = str_host
        self.u_port = u_port
        self.str_user = str_user
        self.str_pwd = str_pwd
        self.str_db_name = str_db_name
        self.str_ssh_domain = str_ssh_domain
        self.str_ssh_user = str_ssh_user
        self.str_ssh_pwd = str_ssh_pwd

class FieldValue(object):
    def __init__(self, str_field_name, value,b_is_not_string = False,u_str_max_len = 0):
        self.str_field_name = str_field_name
        self.value = value             #1：字符串 2：数字  3：NULL
        self.b_is_not_string = b_is_not_string  #是否 '不' 是字符串类型
        self.u_str_max_len = u_str_max_len

class SqlCreate(object):
    def __init__(self):
        self.param_list = []

    def add_insert_param(self,str_field_name,value,b_is_not_string = False,b_is_convert_none = True,u_str_max_len = 0):
        if str_field_name != 'Source_ID' and b_is_convert_none == True:
            if value == -1 or value == '-1' or value == u'-1':
                value = None
        self.param_list.append(FieldValue(str_field_name,value,b_is_not_string,u_str_max_len))

    def add_update_param(self,str_field_name,value,b_is_not_string = False,b_is_convert_none = True,u_str_max_len = 0):
        if str_field_name != 'Source_ID' and b_is_convert_none == True:
            if value == -1 or value == '-1' or value == u'-1':
                value = None
        self.param_list.append(FieldValue(str_field_name,value,b_is_not_string,u_str_max_len))

    def add_insert_params(self,dict_params,list_exclude_field = None):
        for v,k in dict_params.items():
            if list_exclude_field:
                if v not in list_exclude_field:
                    self.add_insert_param(v,k)
            else:
                self.add_insert_param(v,k)

    def generate_update_sql(self,str_table_name,str_where):
        str_update_units = ''

        n = 0
        while n < len(self.param_list):
            field_value = self.param_list[n]
            str_update_unit = ''
            str_update_value = ''
            str_update_field = ''
            if field_value.value == None:
                str_update_value = "NULL"
            elif isinstance(field_value.value,str) == True and field_value.b_is_not_string == False:
                if field_value.u_str_max_len > 0:
                    if len(field_value.value) > int(field_value.u_str_max_len):
                        field_value.value = field_value.value[0:field_value.u_str_max_len - 1]
                        # field_value.value = field_value.value.decode('utf8','ignore')
                        # field_value.value = field_value.value.encode('utf8','ignore')

                field_value.value = MySQLdb.escape_string(field_value.value)
                str_update_value = "'" + field_value.value.decode(encoding='utf-8') +"'"
            else:
                str_update_value = str(field_value.value)

            str_update_field = '`'+field_value.str_field_name+'`'

            str_update_unit = ' '+str_update_field+'='+str_update_value+' '

            if n < len(self.param_list) - 1:
                str_update_unit += ','

            str_update_units += str_update_unit
            n += 1

        str_sql = ''
        str_sql += 'UPDATE `'
        str_sql += str_table_name
        str_sql += '` SET '
        str_sql += str_update_units
        str_sql += " WHERE "
        str_sql += str_where

        return str_sql

    @staticmethod
    def generate_multi_insert_sql(list_sql_create,str_table_name):
        try:

            if len(list_sql_create) <= 0:
                return ''

            sql_create = list_sql_create[0]
            str_sql = ''
            str_sql += 'INSERT INTO `'
            str_sql += str_table_name


            str_field_name = ''

            n = 0
            while n < len(sql_create.param_list):
                field_value = sql_create.param_list[n]
                tmp = ''
                tmp = '`'+field_value.str_field_name+'`'

                if n < len(sql_create.param_list) - 1:
                    tmp += ','

                str_field_name += tmp

                n += 1

            str_sql += '` ('
            str_sql += str_field_name
            str_sql += ") VALUES  "

            m = 0
            for sql_create in list_sql_create:
                str_value = ''
                m += 1
                n = 0
                while n < len(sql_create.param_list):
                    field_value = sql_create.param_list[n]
                    tmp = ''
                    if field_value.value == None:
                        tmp = "NULL"
                    elif isinstance(field_value.value,str) == True and field_value.b_is_not_string == False:
                        tmp_value = field_value.value
                        if field_value.u_str_max_len > 0:
                            if len(field_value.value) > int(field_value.u_str_max_len):
                                tmp_value = field_value.value[0:field_value.u_str_max_len - 1]
                        tmp_value = MySQLdb.escape_string(tmp_value)
                        tmp = "'" + tmp_value.decode(encoding='utf-8') +"'"
                    elif isinstance(field_value.value,bytes) == True and field_value.b_is_not_string == False:
                        tmp_value = field_value.value.decode(encoding='utf-8')
                        if field_value.u_str_max_len > 0:
                            if len(tmp_value) > int(field_value.u_str_max_len):
                                tmp_value = tmp_value[0:field_value.u_str_max_len - 1]
                        tmp_value = MySQLdb.escape_string(tmp_value)
                        tmp = "'" + tmp_value.decode(encoding='utf-8') +"'"
                    elif isinstance(field_value.value,datetime.datetime) == True and field_value.b_is_not_string == False:
                        tmp_value = field_value.value.strftime('%Y-%m-%d %H:%M:%S')
                        tmp = "'" + tmp_value +"'"
                    else:
                        tmp = str(field_value.value)

                    if n < len(sql_create.param_list) - 1:
                        tmp += ','

                    str_value += tmp
                    n += 1

                if m > 1:
                    str_sql += ','
                str_sql += "("+str_value
                str_sql += ")"

            return str_sql
        except Exception as x:
            err = traceback.format_exc()
            pass

    def generate_insert_sql(self,str_table_name):
        try:
            str_field_name = ''
            str_value = ''
            n = 0
            while n < len(self.param_list):
                field_value = self.param_list[n]
                tmp = ''
                tmp = '`'+field_value.str_field_name+'`'

                if n < len(self.param_list) - 1:
                    tmp += ','

                str_field_name += tmp

                n += 1

            n = 0
            while n < len(self.param_list):
                field_value = self.param_list[n]
                tmp = ''
                if field_value.value == None:
                    tmp = "NULL"

                elif isinstance(field_value.value,str) == True and field_value.b_is_not_string == False:
                    tmp_value = field_value.value
                    if field_value.u_str_max_len > 0:
                        if len(field_value.value) > int(field_value.u_str_max_len):
                            tmp_value = field_value.value[0:field_value.u_str_max_len - 1]
                    tmp_value = MySQLdb.escape_string(tmp_value)
                    tmp = "'" + tmp_value.decode(encoding='utf-8') +"'"
                elif isinstance(field_value.value,bytes) == True and field_value.b_is_not_string == False:
                    tmp_value = field_value.value.decode(encoding='utf-8')
                    if field_value.u_str_max_len > 0:
                        if len(tmp_value) > int(field_value.u_str_max_len):
                            tmp_value = tmp_value[0:field_value.u_str_max_len - 1]
                    tmp_value = MySQLdb.escape_string(tmp_value)
                    tmp = "'" + tmp_value.decode(encoding='utf-8') +"'"
                elif isinstance(field_value.value,datetime.datetime) == True and field_value.b_is_not_string == False:
                    tmp_value = field_value.value.strftime('%Y-%m-%d %H:%M:%S')
                    tmp = "'" + tmp_value +"'"
                else:
                    tmp = str(field_value.value)

                if n < len(self.param_list) - 1:
                    tmp += ','

                str_value += tmp
                n += 1

            str_sql = ''
            str_sql += 'INSERT INTO `'
            str_sql += str_table_name
            str_sql += '` ('
            str_sql += str_field_name
            str_sql += ") VALUES  ("
            str_sql += str_value
            str_sql += ")"

            return str_sql
        except Exception as x:
            err = traceback.format_exc()
            pass

class  DbOperBaseException(Exception):
    err_code = {0:'success'
        ,1:'connect database failed'}

    def  __init__ (self, str_msg='', str_err_code_msg='', original_except = None):
        Exception.__init__(self)
        print_msg = []
        print_msg.append(str_msg)
        if isinstance(original_except,Exception) == True:
            print_msg.append(original_except.args)
        self.args = print_msg
        self.str_err_code_msg = str_err_code_msg
        self.original_except =  original_except

class DbOperBase(object):
    str_host='192.168.0.100'
    u_port=3306
    str_user='root'
    str_pwd='888888'
    str_db_name='jy_db'

    class SelectInit():
        def __init__(self,dboper,is_dict_ret = False):
            self.dboper = dboper
            self.b_status = self.dboper.select_init(is_dict_ret)

        def __enter__(self):
            pass

        def __exit__(self, type, value, trace):
            self.dboper.select_uninit(self.b_status)


    #每个进程初始化一次
    @staticmethod
    def static_init():
        DbOperBase.str_host='192.168.0.100'
        DbOperBase.u_port=3306
        DbOperBase.str_user='root'
        DbOperBase.str_pwd='888888'
        DbOperBase.str_db_name='jy_db'

    def __init__(self,str_host = '',u_port = 0, str_user = '', str_pwd = '', str_db_name = '',str_ssh_domain='',str_ssh_user='',str_ssh_pwd=''):
        self._conn = None
        self._cursor = None
        self._ssh_server = None

        if str_host == '':
            self.str_host = DbOperBase.str_host
            self.u_port = DbOperBase.u_port
            self.str_user = DbOperBase.str_user
            self.str_pwd = DbOperBase.str_pwd
            self.str_db_name = DbOperBase.str_db_name
        else:
            self.str_host = str_host
            self.u_port = u_port
            self.str_user = str_user
            self.str_pwd = str_pwd
            self.str_db_name = str_db_name

        self.str_ssh_domain = str_ssh_domain
        self.str_ssh_user = str_ssh_user
        self.str_ssh_pwd = str_ssh_pwd
        self.b_ssh_started = False
        return

    def __del__(self):
        return

    def set_cfg(self,db_cfg):
        self.str_host = db_cfg.str_host
        self.u_port = db_cfg.u_port
        self.str_user = db_cfg.str_user
        self.str_pwd = db_cfg.str_pwd
        self.str_db_name = db_cfg.str_db_name

        self.str_ssh_domain = db_cfg.str_ssh_domain
        self.str_ssh_user = db_cfg.str_ssh_user
        self.str_ssh_pwd = db_cfg.str_ssh_pwd

    def ssh_start(self):
        try:
            if self.str_ssh_domain != '':
                if self._ssh_server:
                    try:
                        self._ssh_server.stop()
                    except Exception:
                        pass
                    self._ssh_server = None
                self._ssh_server = SSHTunnelForwarder(
                         (self.str_ssh_domain, 22),
                         ssh_password=self.str_ssh_pwd,
                         ssh_username=self.str_ssh_user,
                         remote_bind_address=(self.str_host, self.u_port)
                )
                self._ssh_server.start()
                self.b_ssh_started = True
        except Exception as x:
            self.ssh_stop()
            self.b_ssh_started = False

    def ssh_stop(self):
        try:
            if self.str_ssh_domain != '':
                try:
                    self._ssh_server.stop()
                except Exception:
                    pass
            self._ssh_server = None
            self.b_ssh_started = False
        except Exception as x:
            self.b_ssh_started = False

    def close_db_conn(self):
        try:
            if self._conn != None and self.is_connected() == True:
                self._conn.close()

            self._conn = None
        except Exception as x:
            pass
        self._conn = None


    def open_db_conn(self,u_time_out = 30):
        base = 10
        n = 0
        max = u_time_out/base
        while True:
            try:
                if self.str_ssh_domain != '':
                    if n > 0:
                        self.ssh_start()

                    self._conn = None
                    self._conn = MySQLdb.connect(host='127.0.0.1', port=self._ssh_server.local_bind_port,user=self.str_user, passwd=self.str_pwd, db=self.str_db_name, charset='utf8',connect_timeout=base)
                    self._cursor = None
                else:
                    self._conn = None
                    self._conn = MySQLdb.connect(host=self.str_host, port=self.u_port,user=self.str_user, passwd=self.str_pwd, db=self.str_db_name, charset='utf8',connect_timeout=base)
                    self._cursor = None
                return
            except Exception as x:
                time.sleep(0.01)
                n += 1
                if n > max:
                    DbOperBase._err_raise('','',x)

    #数据库连接配置
    @staticmethod
    def set_db_cfg(str_host, u_port,str_user, str_passwd, str_db):
        DbOperBase.str_host = str_host
        DbOperBase.u_port = u_port
        DbOperBase.str_user = str_user
        DbOperBase.str_pwd = str_passwd
        DbOperBase.str_db_name = str_db

    @staticmethod
    def _err_raise(str_param = '',str_err_code_msg = '',original_except = None):
        str_msg = '--database_oper :'+str(sys._getframe().f_back.f_lineno)+':'+sys._getframe().f_back.f_code.co_name+':'+str_param+':'+str_err_code_msg
        raise DbOperBaseException(str_msg,str_err_code_msg,original_except)

    def is_connected(self):
        try:
            self._conn.ping()
        except Exception as x:
            return False

        return True

    def trans_begin(self, is_dict_ret = False):
        try:
            if is_dict_ret == False:
                self._cursor = self._conn.cursor()
            else:
                self._cursor = self._conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def trans_rollback(self):
        try:
            self._cursor.close()
            self._conn.rollback()
            self._cursor = None
        except Exception as x:
            pass

    def trans_commit(self):
        try:
            self._cursor.close()
            self._conn.commit()
            self._cursor = None
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def fetchall(self):
        try:
            rows = self._cursor.fetchall()
            return rows
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def fetchone(self):
        try:
            row = self._cursor.fetchone()
            return row
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def execute(self,str_sql):
        try:
            self._cursor.execute(str_sql)
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def affect_rowcount(self):
        try:
            return self._cursor.rowcount
        except Exception as x:
            DbOperBase._err_raise('','',x)

    def last_rowid(self):
        try:
            return self._cursor.lastrowid
        except Exception as x:
            DbOperBase._err_raise('','',x)


    def select_init(self, is_dict_ret = False):
        b_cursor_is_init = True
        if self._cursor == None:
            b_cursor_is_init = False
            if is_dict_ret == False:
                self._cursor = self._conn.cursor()
            else:
                self._cursor = self._conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)

        return b_cursor_is_init

    def select_uninit(self,b_cursor_is_init):
        if b_cursor_is_init == False:
            self._cursor.close()
            self._cursor = None

    def get_columns(self, str_table_name):
        str_sql = ''
        b_cursor_is_init = False
        try:
            str_sql = "select `COLUMN_NAME` from information_schema.COLUMNS where `table_name` = '%s' and `table_schema` = '%s';"%(str_table_name, self.str_db_name)

            b_cursor_is_init = True
            if self._cursor == None:
                b_cursor_is_init = False
                self._cursor = self._conn.cursor()
            # 执行sql语句
            self._cursor.execute(str_sql)

            rows = self._cursor.fetchall()

            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None

            return rows

        except Exception as x:
            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None
            return -1

    def get_records_count(self, str_table_name,str_condition = ''):
        str_sql = ''
        b_cursor_is_init = False
        try:
            str_sql = "select count(*) from %s"%str_table_name
            if str_condition != '':
                str_sql += ' WHERE '
                str_sql += str_condition

            b_cursor_is_init = True
            if self._cursor == None:
                b_cursor_is_init = False
                self._cursor = self._conn.cursor()
            # 执行sql语句
            self._cursor.execute(str_sql)

            row = self._cursor.fetchone()

            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None

            return row[0]

        except Exception as x:
            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None
            return -1

    def get_db_time(self):
        str_sql = ''
        b_cursor_is_init = False
        try:
            str_sql = "SELECT NOW()"

            b_cursor_is_init = True
            if self._cursor == None:
                b_cursor_is_init = False
                self._cursor = self._conn.cursor()
            # 执行sql语句
            self._cursor.execute(str_sql)

            row = self._cursor.fetchone()

            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None

            return row[0]

        except Exception as x:
            if b_cursor_is_init == False:
                self._cursor.close()
                self._cursor = None
            return -1

    @staticmethod
    def common_select(str_sql,dboper, db_cfg = None,is_multi_row_ret = False, is_dict_ret = True):
        """
        通用查询
        :param str_sql:查询语句
        :param dboper:连接对象
        :param db_cfg:连接配置
        :param is_multi_row_ret: 是否返回多行
        :param is_dict_ret: 是否用字典的形式返回结果集
        :return:结果集

        注：dboper 与 db_cfg 只能有一个为None
        """
        curr_dboper = None
        is_connect = False
        try:
            if dboper:
                curr_dboper = dboper
            elif db_cfg:
                dboper = DbOperBase(db_cfg.str_host,db_cfg.u_port,db_cfg.str_user,db_cfg.str_pwd,db_cfg.str_db_name,db_cfg.str_ssh_domain,db_cfg.str_ssh_user,db_cfg.str_ssh_pwd)
                curr_dboper = dboper
                is_connect = True
            else:
                return None

            if curr_dboper.is_connected() == False:
                is_connect = True
                curr_dboper.ssh_start()
                curr_dboper.open_db_conn()

            row = None
            with DbOperBase.SelectInit(dboper,is_dict_ret):
                try:

                    # 执行sql语句
                    curr_dboper._cursor.execute(str_sql)

                    if is_multi_row_ret == True:
                        row = curr_dboper._cursor.fetchall()
                    else:
                        row = curr_dboper._cursor.fetchone()

                except Exception as x:
                    pass

            if is_connect:
                curr_dboper.close_db_conn()
                curr_dboper.ssh_stop()

            if row != None and len(row) > 0:
                if isinstance(row,tuple) == True:
                    row = list(row)
                return row
            else:
                return None

        except Exception as x:
            if curr_dboper and is_connect:
                curr_dboper.close_db_conn()
                curr_dboper.ssh_stop()
            return None