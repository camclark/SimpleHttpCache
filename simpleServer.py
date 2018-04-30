from http.server import HTTPServer, BaseHTTPRequestHandler
import redis
import time

CACHE_SERVER_PORT_NUMBER = 8000
CACHE_SERVER_ADDRESS = 'localhost'

REDIS_SERVER_PORT_NUMBER = 6379
REDIS_SERVER_ADDRESS = 'localhost'

# create instance of server
r = redis.Redis(
    host=REDIS_SERVER_ADDRESS,
    port=REDIS_SERVER_PORT_NUMBER)

# test set
r.set('foo', {'bar': 'bar2'})
r.expire('foo', 30)
print('set')


class ServerCacheHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # test get
        value = r.get('foo')
        print(value)
        print(type(value))

        time.sleep(31)
        # test get to fail as TTL has expired
        value = r.get('foo')
        print(value)
        print(type(value))

        if value is None:
            print("Resource not found", "add appropriate response code")

        return

    def do_POST(self):
        pass


def run():
    server_url = (CACHE_SERVER_ADDRESS, CACHE_SERVER_PORT_NUMBER)
    http_start = HTTPServer(server_url, ServerCacheHandler)
    print("Server Started, Running on Port: ", CACHE_SERVER_PORT_NUMBER)
    http_start.serve_forever()


if __name__ == '__main__':
    run()
