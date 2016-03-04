from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from boto import kinesis

PORT_NUMBER = 8080
LOG_FILE = '/tmp/mobile_requests.log'
KINESIS_AWS_REGION = 'us-west-2'
KINESIS_STREAM_NAME = 'mobile_logs'
KINESIS_PARTITION_KEY = 'partitionKey'


def init_kinesis():
    k = kinesis.connect_to_region(KINESIS_AWS_REGION)
    if KINESIS_STREAM_NAME not in k.list_streams()['StreamNames']:
        k.create_stream(KINESIS_STREAM_NAME, 1)
    return k

class Handler(BaseHTTPRequestHandler):

    klc = init_kinesis()

    def do_POST(self):
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        data = self.format_data(body)
        self.ok()
        self.log_to_disk(data)
        self.log_to_kinesis(data)

    def format_data(self, data):
        return data + '\n'

    def log_to_disk(self, data):
        with open(LOG_FILE, 'a') as f:
            f.write(data)

    def log_to_kinesis(self, data):
        self.klc.put_record(KINESIS_STREAM_NAME, data, KINESIS_PARTITION_KEY)

    def ok(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('{"status": "ok"}')

def main():
    try:
        server = HTTPServer(('', PORT_NUMBER), Handler)
        print 'Server is listening at port', PORT_NUMBER
        server.serve_forever()
    except KeyboardInterrupt:
        print '\nCtrl+C received, shutting down the server'
        server.socket.close()

if __name__ == '__main__':
    main()
