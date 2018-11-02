import pymysql
import pymysql.cursors


# 获取数据库链接
def getConnection():
    dest = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'db': 'datawork'
    }
    return pymysql.connect(**dest)


class SqlTool(object):
    insert_url_sql = 'insert into url(url) values(%s)'
    insert_page_sql = 'insert into page(url_id, content) values(%s,%s)'
    insert_url_out_sql = 'insert into url_out(st_url_id, ed_url_id) values(%s,%s)'
    select_url_sql = 'select id,url from url where url=%s'

    def __init__(self, connection):
        self.connection = connection

    # 向表url 中插入数据
    def insert_url(self, url):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(SqlTool.insert_url_sql, (url,))
                self.connection.commit()
                return cursor.lastrowid
        except:
            self.connection.rollback()

    # 查询该url 是否存在
    def select_url(self, url):
        with self.connection.cursor() as cursor:
            cursor.execute(SqlTool.select_url_sql, (url,))
            result = cursor.fetchone()
            return result

    # 向表page 中插入数据
    def insert_page(self, url_id, content):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(SqlTool.insert_page_sql, (url_id, content))
                self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()

    # 向表 url_out 中插入数据
    def insert_url_out(self, st_url_id, ed_url_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(SqlTool.insert_url_out_sql, (st_url_id, ed_url_id))
                self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()

    def __del__(self):
        self.connection.close()
