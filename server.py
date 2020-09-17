import asyncio
import time


class Storage:
    """Класс, выполняющий роль хранилища метрик"""

    def __init__(self):
        self._data = {}

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        if key not in self._data:
            self._data[key] = {}

        self._data[key][timestamp] = value

    def get(self, key):
        data = self._data

        if key != "*":
            data = {key: data.get(key, {})}

        result = {}

        for key, timestamp_data in data.items():
            result[key] = sorted(timestamp_data.items())

        return result
