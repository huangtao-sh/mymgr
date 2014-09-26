
Mysql 连接库函数
====

开发目的
---

* 共享同一数据库连接

整个程序只用建立一次连接即可，其他的模块只需要执行SQL语句即可，
以简化程序的开发过程。对于复杂的程序，主程序负责连接的维护，
其他模块只用查其查询模块即可。

* 简化调用方式

抽象出几种标准的调用模式，使程序不用考虑如何去与数据库对接。

主要功能
----
- 属性

	1. connected

	bool型，只读，数据库是否已连接

	2. cursor

	游标，只读
	
- 连接数据库

	1. connect(**kwargs),连接数据库，连接成功后相关参数将被保存，如果kwargs为空，则使用当前连接数据。
	2. disconnect(),断开数据库连接
- 调用存储过程

	1. call\_proc(proc\_name,params,call\_back)，返回值为params。如返回查询结果，则必须使用call\_back函数读取，否则，	如call\_back未送，放弃查询结果。
	
- 查询数据

	1. query(sql,params=None,call\_back=None)
	执行查询，如call\_back上送，则由call\_back处理查询结果，如未上送，
	则返回cursor
	2. query_str(sql,params=None)
	查询字符串，直接返回查询到的字符串。
	3. query\_list(sql,params,direction=0)
	查询列表数据，如direction为0，则查询一列数据；
	如direction为非0数据，则查询一行数据。

- 执行SQL语句

	1. execute(sql,params=None)
	执行SQL语句。
	
	2. execute_many(sql,param\_list)
	使用不同的参数执行同一条语句。执行次数取决于param\_list数量。

- 线程中执行

	1. tquery(self,sql,params=None,call_back=None)
	参数同query，数据连接及call\_back均在线程中执行。

	2. texec(self,sql,param_list)
	参数同exec\_many,数据库的连接及SQL语句均在线程中执行

典型的使用
----
    
		class A(MyMgr):
			pass
		class B(MyMgr):
			pass
    
		a=A()
		a.connect(host='loacalhost',user='',passwd='',db='')
		b.texec('insert into ab values(%s,%s)',param_list=param_list)
	    b.call_proc('proc_name',params=params,call_back=call_back)
		a.disconnect()

依赖
---
本程序需要使用MySQL Connectors模块，可以在
[MySQL](http://www.mysql.com/products/connector/)进行下载后安装。



