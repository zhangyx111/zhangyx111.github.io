# migrate_database.py
import pymysql
from sqlalchemy import create_engine
import pandas as pd

def migrate_database():
    # 源数据库（服务器）
    source_conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123',
        port=3306,
        database='caslip_news'
    )
    
    # 目标数据库（本地）
    target_engine = create_engine('mysql+pymysql://root:password@localhost:3306/caslip_news_local')
    
    try:
        # 获取所有表名
        with source_conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
        
        print(f"找到 {len(tables)} 个表需要迁移")
        
        for table in tables:
            print(f"迁移表: {table}")
            
            # 从源数据库读取数据
            df = pd.read_sql(f"SELECT * FROM {table}", source_conn)
            
            # 写入目标数据库
            df.to_sql(table, target_engine, if_exists='replace', index=False)
            
            print(f"  ✅ 完成 {len(df)} 条记录")
    
    finally:
        source_conn.close()

if __name__ == '__main__':
    migrate_database()