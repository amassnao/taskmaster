
HOST = "127.0.0.1"
PORT = 4242

def read(conn, buffer=1024):
    data = ''
    while conn:
        r = conn.recv(buffer)
        data += r.decode('utf-8')
        if len(r) < buffer:
            break
    return data

def write(conn, data=''):
    conn.sendall(bytes(data, 'utf-8'))