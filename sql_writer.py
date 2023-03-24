import mysql.connector


class MySQLWritter:

    def __init__(self, host = None, user = None, password = None, database = None, port = None, **kwargs):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.kwargs = kwargs

    def init_conn(self):
        if self.user is None:
            config = {
                'user': 'user',
                'password': 'test',
                'host': 'localhost',
                'port': '3306',
                'database': 'order'
            }
        else:
            config = {
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'database': self.database
            }
        self.conn = mysql.connector.connect(**config)

    def execute_sql(self, sql):
        self.init_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        self.close_conn()

    def execute_batch_sql(self, sql, value_list):
        self.init_conn()
        cursor = self.conn.cursor()
        cursor.executemany(sql,value_list)
        self.conn.commit()
        cursor.close()
        self.close_conn()

    def execute_and_return(self, sql):
        self.init_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            yield row
        cursor.close()
        self.close_conn()

    def close_conn(self):
        if self.conn.is_connected():
            self.conn.close()
        self.conn = None
