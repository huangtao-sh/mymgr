#!/usr/bin/python3
from mymgr import MyMgr

#回调函数
def call_back(cur):
    for r in cur:
        print(r)

if __name__=='__main__':    
    m=MyMgr()
    mysql_cnf={
            'host':'localhost',
            'user':'hunter',
            'passwd':'123456',
            'db':'test',}
    m.connect(**mysql_cnf)
    sql='''
    insert into ab values(1,%s)
    '''
    #execute语句测试
    m.execute(sql,params=('sdfsf',))
    #query语句查询
    m.query('select * from ab',call_back=call_back)

    m.execute('insert into ab values(%s,%s)',params=(5,'王五'))
    k=m.query('select * from ab',call_back=call_back)
    print(m.query_str('select name from ab where id=%s',params=('3',)))
    k=m.query_list('select * from ab where id>%s',params=(3,),direction=1)
    print(k)
   
    m.disconnect()
