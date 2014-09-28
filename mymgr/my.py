#!/usr/bin/python3
#  MySQL 处理模块
#  作者：黄涛
#  创建：2014-7-21
#  调用方法：exec(sql)
#            query(sql,proc)

from mysql import connector
from threading import Thread

class MyMgr:
    '''
    MySQL连接组件
    用法：
        m=MyMgr(**mysql_cnf)
        m.execute(sql,params)执行SQL语句
        m.query(sql,params,proc)执行查询，其中proc为回调函数
        m.exec_many(sql,params)批量执行SQL语句
        m.texec(sql,params)使用线程批量执行SQL语句
        m.tquery(sql,params,proc)使用线程执行查询，其中proc为回调函数
    '''
    #采用字典保存数据用于跨模块共享连接数据
    _data={
        'config':None,
        'connection':None,
        'cursor':None,
        'connected':False,
        }

    @property
    def connected(self):
        return self._data['connected']

    @property
    def cursor(self):
        return self._data['cursor']

    def connect(self,**kwargs):
        if self.connected:
            self.disconnect()
        if kwargs:
            self._data['config']=kwargs
        try:
            self._data['connection']=connector.connect(
                **self._data['config'])
        finally:
            self._data['cursor']=self._data['connection'].cursor()
            self._data['connected']=True

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self._data['connection']:
                self._data['connection'].close()
        finally:
            self._data['cursor']=None
            self._data['connection']=None
            self._data['connected']=False
    
    def call_proc(self,proc_name,params=None,call_back=None):
        if self.connected:
            d=self.cursor.callproc(proc_name,params)
            if call_back:
                data=[result for result in self.cursor.stored_results()]
                call_back(data[0]if len(data)==1 else data)
            return d

    def commit(self):
        self._data['connection'].commit()
        
    def execute(self,sql,params=None):
        '''
        执行单一SQL语句
        参数说明：
            sql:SQL语句，如"select * from T1 where dt=%s"
            params:SQL语中的变量，形式如(123,'hunter')
        '''
        self.query(sql,params)
        self.commit()
    
    @staticmethod
    def split_data(data,step=10000):
        b,e=0,0
        count=len(data)
        for e in range(step,count,step):
            yield data[b:e]
            b=e
        if e<count:
            yield data[e:count]

    def exec_many(self,sql,param_list):
        '''
        执行多条SQL语句
        参数说明：
            sql:SQL语句
            sql_params:SQL语句中的变量，形式如：(('123',12),('456',45))
        '''
        if self.connected:
            try:
                for params in self.split_data(param_list):
                    self.cursor.executemany(sql,params)
                self.commit()
            except BaseException as err:
                print(err)

    def query(self,sql,params=None,call_back=None):
        '''
        执行SQL查询，查询成功后调用proc函数
        参数说明：
            sql:SQL语句
            params:参数值，形式如：('123',45)
            proc：回调函数，原型为：proc(__cursor)
        '''
        if self.connected:
            self.cursor.execute(sql,params=params)
            if call_back:
                call_back(self.cursor)
            else:
                return self.cursor

    def query_str(self,sql,params=None):
        self.query(sql,params)
        d=self.cursor.fetchall()
        if d:
            return d[0][0]

    def query_list(self,sql,params=None,direction=0):
        self.query(sql,params)
        d=self.cursor.fetchall()
        if d:
            return d[0]if direction else tuple(r[0] for r in d)
        
    def exec_thread(self,func,arg):
        if self.connected:
            try:
                m=MyMgr()
                m._data={
                    'config':None,
                    'connection':None,
                    'cursor':None,
                    'connected':False,
                }
                m.connect(**self._data['config'])
                Thread(target=func(m,*arg)).start()
            finally:
                m.disconnect()

    def texec(self,sql,param_list):
        '''
        使用线程执行SQL语句。参数说明同execmany
        '''
        self.exec_thread(MyMgr.exec_many,(sql,param_list))

    def tquery(self,sql,params=None,call_back=None):
        '''
        使用线程执行查询，参数说明同query
        '''
        self.exec_thread(MyMgr.query,[sql,params,call_back])

