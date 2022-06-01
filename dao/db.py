import time
import pymysql


class RobotData:
    def __init__(self, db_host: str, db_port: int,
                 db_user: str, db_pwd: str,
                 db_db: str, db_timeout: int):
        self._host = db_host
        self._port = db_port
        self._user = db_user
        self._pwd = db_pwd
        self._database = db_db
        self._timeout = db_timeout
        self._db = None
        self._cursor = None
        self._conn()

    def _conn(self):
        try:
            self._db = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._pwd,
                database=self._database,
                connect_timeout=self._timeout
            )
            self._cursor = self._db.cursor()
            return True
        except:
            return False

    def _re_conn(self, num=28800, sleep_time=3):  # retry for 1 day
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self._db.ping()
                _status = False
            except:
                if self._conn():
                    _status = False
                    break
                _number += 1
                time.sleep(sleep_time)  # failed and sleep

    def close(self):
        self._db.close()

    def get_version(self) -> str:
        self._re_conn()
        self._cursor.execute('select version()')
        data = self._cursor.fetchone()
        return "database version is [%s]" % data

    def do_select(self, sql) -> tuple:
        self._re_conn()
        self._cursor.execute(sql)
        data = self._cursor.fetchall()
        return data

    def do_select_cnt(self, sql) -> int:
        self._re_conn()
        self._cursor.execute(sql)
        data = self._cursor.fetchone()
        return int(data[0])

    def do_insert(self, sql, params) -> str:
        self._re_conn()
        self._cursor.execute(sql, params)
        self._db.commit()
        return ""

    def do_update(self, sql, params) -> str:
        self._re_conn()
        self._cursor.execute(sql, params)
        self._db.commit()
        return ""

