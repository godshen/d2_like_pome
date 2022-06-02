import redis as rd


class RobotCache:
    def __init__(self):
        self._host = "0.0.0.0"

    def _conn(self):
        self._c = rd.Redis(
            host=self._host
        )

    def get_data(self, key):
        return self._c.get(key)