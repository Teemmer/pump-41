import socket
import sys
import traceback
import functools 

def response_ok(body=b"<html><h1>MyServer Homepage</h1></html>", mimetype=b"text/html"):
    response = b'''HTTP/1.1 200 OK\r\n
        Content-Type: {0}\r
        Age: 0\r
        Keep-Alive: max=0\r
        \r\n
        {1}\r
        '''.format(mimetype, body)
    return response


def response_not_found(path):
    """Returns a 404 Not Found response"""
    response = b'''HTTP/1.1 404 Not Found\r\n
                Content-Type: text/html\r
                Age: 0\r
                Keep-Alive: max=0\r
                <html><h1>{} not found!</h1></html>\r\n
                '''.format('/'.join(path))
    return response


def parse_request(request):
    uri = request.split()[1].split('/')
    path = [r for r in uri if len(r) > 0 and r[0] != '?']
    params = [r for r in uri if len(r) > 0 and r[0] == '?']
    params = params[0][1:].split('&') if params else params
    params = {x: y for [x, y] in map(lambda s: s.split('='), params)}
    return path, params


def number(path, params):
    if len(path) == 1 or path[1] == 'add':
        return functools.reduce(lambda a, b: float(a) + float(b), params.values())
    return functools.reduce(lambda a, b: float(a) * float(b), params.values())


def stringg(params):
    if not params.get('str'):
        return None
    result = params.get('str')
    if 'reverse' in params.keys():
        if params['reverse'] == '1':
            result = result[::-1]
    return result



def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address))
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection')
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr))

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break
		

                print("Request received:\n{}\n\n".format(request))
                path, params = parse_request(request)

                if path and path[0] in ['num', 'str']:
                    if path[0] == 'num':
                        response = response_ok(
                            body=number(path, params),
                            mimetype='text/plain'
                            )
                    else:
                        response = response_ok(
                            body=stringg(params),
                            mimetype='text/plain'
                            )
                elif path:
                    response = response_not_found(path)
                else:
                    response = response_ok()

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)