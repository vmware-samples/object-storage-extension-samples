import psycopg2


'''
CREATE: cur.execute(
        'CREATE TABLE Employee ('
        'name    varchar(80),'
        'address varchar(80),'
        'age     int,'
        'date    date'
        ')'
    )

cur.execute("INSERT INTO Employee "
        "VALUES('Gopher', 'China Beijing', 100, '2017-05-27')")
        
cur.execute("SELECT * FROM Employee")

cur.execute("UPDATE Employee SET age=12 WHERE name='Gopher'")

cur.execute("DELETE FROM Employee WHERE name='Gopher'")


'''


class DBClient:
    def __init__(self, dbhost, dbport, db_name, dbuser, dbpassword):
        self.host = dbhost
        self.port = dbport
        self.db_name = db_name
        self.user = dbuser
        self.password = dbpassword
        self.conn = self.cur = None

        self.conn = psycopg2.connect(host=self.host, port=self.port,
                                     database=self.db_name, user=self.user,
                                     password=self.password)
        print("Opened database successfully")
        self.cur = self.conn.cursor()

    def cur_query(self, sql_cmd):
        self.cur.execute(sql_cmd)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def cur_execute(self, sql_cmd):
        self.cur.execute(sql_cmd)

    def conn_commit(self):
        self.conn.commit()

    def cur_close(self):
        self.cur.close()
        self.conn.close()

    def empty_table(self, table_n):
        self.conn = psycopg2.connect(host=self.host, port=self.port,
                                     database=self.db_name, user=self.user,
                                     password=self.password)
        print("Opened database successfully")
        self.cur = self.conn.cursor()

        sql_cmd = 'delete from %s;' % table_n
        self.cur.execute(sql_cmd)

        sql_cmd = 'select * from %s;' % table_n
        self.cur.execute(sql_cmd)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

        self.cur.close()
        self.conn.close()

    def drop_table(self, table_n):
        sql_cmd = 'DROP TABLE %s;' % table_n
        self.cur.execute(sql_cmd)


if __name__ == '__main__':
    # db_c = DBClient('10.110.124.129', 5432, 'ossdb', 'ossdb', 'VMware1!')
    # db_c.drop_table(table_n='config_info')
    # db_c.delete('')
    db_c = DBClient('10.110.124.130', 5432, 'voserst', 'vose_user', 'ca$hc0w')
    '''
    sql_cmd_1 = "INSERT INTO test_run VALUES ('2019-11-09 12:12:13', 'qe_env', 'qe_web', 'https://xxx.com/id', '2019-11-09 12:12:13')"
    db_c.cur_execute(sql_cmd=sql_cmd_1)

    db_c.conn_commit()
    '''
    sql_cmd = 'select * from test_run;'
    db_c.cur_query(sql_cmd)
    db_c.cur_close()

