from http.server import HTTPServer, BaseHTTPRequestHandler
import redis
import re
import cgi
import json
import urllib

CACHE_SERVER_PORT_NUMBER = 8000
CACHE_SERVER_ADDRESS = 'localhost'

REDIS_SERVER_PORT_NUMBER = 6379
REDIS_SERVER_ADDRESS = 'localhost'

# create instance of server
r = redis.Redis(
    host=REDIS_SERVER_ADDRESS,
    port=REDIS_SERVER_PORT_NUMBER)

# # test set
# r.set(2019, {'id': 2019, 'message': 'Telstra 2019 Graduate Program'})
# r.expire('2019', 30)


# print('set')

class ServerCacheHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if None is not re.search('/messages/*', self.path):
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
        if None is not re.search('messages/*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.get_all('content-length')[0])
                print(length)
                # print(length)
                post_data = self.rfile.read(length)
                post_json_dict = json.loads(post_data)
                print(type(post_json_dict))
                print(post_json_dict["id"])
                print(post_json_dict["message"])



                # print("Type", type(self.rfile.read(length)))
                # print(pdict)
                # print(json.loads(pdict))


                # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

                # # urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=True, strict_parsing=False,
                #                       encoding='utf-8',
                #                       errors='replace')
                #
                # # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                # # recordID = self.path.split('/')[-1]
                # # obj = json.loads(data)
                # # LocalData.records[recordID] = data
                #
                #
                # # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                # # recordID = self.path.split('/')[-1]
                # # LocalData.records[recordID] = data
                # # print("record %s is added successfully" % recordID)


                # # display back
                # import json
                # json_string = json.dumps(YOUR_DATA_STRUCTURE_TO_CONVERT_TO_JSON)
                # self.wfile.write(json_string)

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
