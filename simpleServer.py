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


class ServerCacheHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # check correct path
        if None is not re.search('/messages/*', self.path):
            # get id from url
            record_id = self.path.split('/')[-1]
            record = r.get(record_id)

            # if record exists
            if record is not None:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(record)
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
        # check correct path
        if None is not re.search('messages/*', self.path):
            # use common graphical interface to get content_type
            content_type, p_dict = cgi.parse_header(self.headers.get('content-type'))
            if content_type == 'application/json':
                length = int(self.headers.get_all('content-length')[0])
                post_data = self.rfile.read(length)
                post_json_dict = json.loads(post_data)

                # saved # TODO: make TTL variable
                r.set(post_json_dict["id"], {'id': post_json_dict["id"], 'message': post_json_dict["message"]})
                r.expire(post_json_dict["id"], 30)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

            else:
                self.send_response(200)
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        pass


def run():
    server_url = (CACHE_SERVER_ADDRESS, CACHE_SERVER_PORT_NUMBER)
    http_start = HTTPServer(server_url, ServerCacheHandler)
    print("Server Started, Running on Port: ", CACHE_SERVER_PORT_NUMBER)
    http_start.serve_forever()


if __name__ == '__main__':
    run()
