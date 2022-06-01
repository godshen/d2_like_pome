import pymysql


class RobotData:
    def __init__(self, db_host: str, db_port: int,
                 db_user: str, db_pwd: str,
                 db_db: str, db_timeout: int):
        self._db = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pwd,
            database=db_db,
            connect_timeout=db_timeout
        )
        self._cursor = self._db.cursor()

    def close(self):
        self._db.close()

    def get_version(self) -> str:
        self._cursor.execute('select version()')
        data = self._cursor.fetchone()
        return "database version is [%s]" % data

    def do_select(self, sql) -> tuple:
        self._cursor.execute(sql)
        data = self._cursor.fetchall()
        return data

    def do_select_cnt(self, sql) -> int:
        self._cursor.execute(sql)
        data = self._cursor.fetchone()
        return int(data[0])

    def do_insert(self, sql, params) -> str:
        self._cursor.execute(sql, params)
        self._db.commit()
        return ""

