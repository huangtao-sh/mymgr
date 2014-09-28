#!/usr/bin/python3
from mymgr import MyMgr

class A(MyMgr):
    cnf={
            'host':'localhost',
            'user':'hunter',
            'passwd':'123456',
            'db':'test',}
    def __init__(self):
        self.connect(**self.cnf)
    def terminate(self):
        print('Terminated')
        

class B(MyMgr):
    def do_query(self):
        self.query('select * from ab',call_back=self.call_back)

    def do_tquery(self):
        self.tquery('select * from ab',call_back=self.call_back)

    def call_back(self,cur):
        for r in cur:
            print(r)


#回调函数
def call_back(cur):
    for r in cur:
        print(r)

if __name__=='__main__':
    a=A()
    b=B()
    b.do_query()
    print('线程查询测试')
    b.do_tquery()
    a.terminate()
    
    '''
    m=MyMgr()
    mysql_cnf=
    m.connect(**mysql_cnf)
    print(m._data)
    #execute语句测试
    print('execute 测试，清空测试表格')
    m.execute(sql)
    print('插入数据')
    m.execute('insert into ab values(1,"list")');
    #query语句查询
    print('query 查询')
    m.query('select * from ab',call_back=call_back)

    print('Thread Query Test')
    m.tquery('select * from ab',call_back=call_back)
    print(m._data)
    m.texec('insert into ab values(%s,%s)',
            param_list=((4,'asb'),(5,'awer')));
    m.execute('insert into ab values(%s,%s)',params=(56,'王五1'))
    k=m.query('select * from ab',call_back=call_back)
    #print(m.query_str('select name from ab where id=%s',params=('3',)))
    #k=m.query_list('select * from ab where id>%s',params=(3,),direction=1)
    #print(k)
    print(m._data)
    m.disconnect()
    '''
