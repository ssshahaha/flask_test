# 数据库配置

> MySQL: config.py -> SQLALCHEMY_DATABASE_URI  
Redis: config.py -> DB_RedisUri

# 初始化数据库

> 初始化MySQL表:  
1.cd到server目录内运行alembic init alembic  
2.修改生成的alembic.ini中的sqlalchemy.url  
3.修改生成的alembic文件夹内的env.py文件，其中的target_metadata修改成项目内数据库Base对象  
4.运行alembic revision --autogenerate -m "commit message"  
5.alembic upgrade head  
6.如果报错需运行alembic stamp head后修改对应代码错误后从alembic revision...开始重新执行 7.更新表只需要从alembic revision...开始执行
