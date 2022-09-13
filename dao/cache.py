import redis as rd


class RobotCache:
    def __init__(self):
        self._host = "0.0.0.0"
        self._conn()

    def _conn(self):
        self._c = rd.Redis(
            host=self._host,
            port=6379,
        )

    def get_data(self, key):
        return self._c.get(key).decode("utf-8")

    def set_data(self, key, val):
        return self._c.set(key, val)

    def rm_data(self, key):
        return self._c.delete(key)

    def sadd_data(self, key, uid):
        return self._c.sadd(key, uid)

    def smembers_data(self, key):
        return self._c.smembers(key)

    def lrange_data(self, key):
        return self._c.lrange(key, 0, 6)

    def lpush_data(self, key, data_list):
        for u in data_list:
            self._c.lpush(key, u)
        return 0
