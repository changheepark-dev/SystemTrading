import sqlite3
from api.time_helper import *


# 유니버셜 테이블 없으면 생성
def check_table_exist(db_name, table_name):
    with sqlite3.connect('{}.db'.format(db_name)) as con:
        cur = con.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table' and name=:table_name"
        cur.execute(sql, {"table_name": table_name})

        if len(cur.fetchall()) > 0:
            return True
        else:
            return False


def insert_df_to_db(db_name, table_name, df, option="replace"):
   with sqlite3.connect('{}.db'.format(db_name)) as con:
       df.to_sql(table_name, con, if_exists=option)


def execute_sql(db_name, sql, param={}):
   with sqlite3.connect('{}.db'.format(db_name)) as con:
       cur = con.cursor()
       cur.execute(sql, param)
       return cur



def last_order_check_db(table_name, code, score):
    with sqlite3.connect('C:/TR/SystemTrading/strategy/LOC.db') as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS {}(code varchar(6) PRIMARY KEY, score float(30) NOT NULL, day varchar(8) NOT NULL)".format(table_name))

        today = check_before_open()
        cur.execute("SELECT * FROM %s WHERE day='%s'" % (table_name ,today))  # %s %d %f
        if not cur.fetchone():
            cur.execute("DELETE FROM {}".format(table_name))

        cur.execute("SELECT * FROM %s WHERE code='%s'" % (table_name ,code))  # %s %d %f
        if cur.fetchone():
            cur.execute("UPDATE %s SET score='%f' WHERE code='%s'" % (table_name, score, code))
        else:
            sql = "insert into {}(code, score, day) values (?, ?, ?)".format(table_name)
            cur.execute(sql, (code, score, today))

        return




if __name__ == "__main__":
    pass