from http.server import HTTPServer, BaseHTTPRequestHandler
import redis
import re
import cgi
import json

CACHE_SERVER_PORT_NUMBER = 8000
CACHE_SERVER_ADDRESS = 'localhost'

REDIS_SERVER_PORT_NUMBER = 6379
REDIS_SERVER_ADDRESS = 'localhost'

# create instance of server
r = redis.Redis(
    host=REDIS_SERVER_ADDRESS,
    port=REDIS_SERVER_PORT_NUMBER)

# test set
r.set(2019, {'id': 2019, 'message': 'Telstra 2019 Graduate Program'})
r.expire('2019', 30)
# print('set')

class ServerCacheHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if None != re.search('/messages/*', self.path):
            recordID = self.path.split('/')[-1]
            record = r.get(recordID)

            if record is not None:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(record)
                print(record)
                print(type(record))
                # TODO: fix json encoding
            else:
                self.send_response(400, 'Bad Request: Record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write("Resource not found".encode("utf-8"))

        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write("Forbidden".encode("utf-8"))

    def do_POST(self):
        pass


def run():
    server_url = (CACHE_SERVER_ADDRESS, CACHE_SERVER_PORT_NUMBER)
    http_start = HTTPServer(server_url, ServerCacheHandler)
    print("Server Started, Running on Port: ", CACHE_SERVER_PORT_NUMBER)
    http_start.serve_forever()


if __name__ == '__main__':
    run()
