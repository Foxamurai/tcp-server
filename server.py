import asyncio
import time


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(Server, host, port)

    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


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

        result = "ok\n"

        if key == "*":
            for key in data.keys():
                for timestamp, value in sorted(data[key].items()):
                    result += f"{key} {timestamp} {value}\n"
            result += "\n"

        return result



class Server(asyncio.Protocol):
    def __init__(self):
        self.storage = Storage()

    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, data):
        request = data[:-1].split()
        command = request[0]
        query = request[1:]

        if command == "put":
            key, value, timestamp = query
            self.storage.put(key, value, timestamp)
            return "ok\n\n"
        if command == "get":
            key = query[0]
            raw_data = self.storage.get(key)
            response = ""

    def data_received(self, data):
        request = self.process_data(data.decode())
        self.transport.write(request.encode())



if __name__ == '__main__':
    run_server("127.0.0.1", 8888)
