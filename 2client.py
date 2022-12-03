import socket

clientname = 'rahul'
data = {
        '0791':'Internet Protocol',
        '0792':'Internet Control Message Protocol',
        '1622':'Pip Header Processing'
    }

def add_method(server,key,data):
    dat = f"ADD {key} P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\nTitle: {value}\n\n"
    server.send(bytes(dat,'utf-8'))

if __name__=='__main__':

    p2p = socket.socket()
    clientip=socket.gethostbyname(socket.gethostname())
    p2p.bind((clientip,0))
    p2psockname = p2p.getsockname()[1]

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((socket.gethostname(), 7734))
    print(f'Connted to server {server.getsockname()} {server.getpeername()}')
    
    for key,value in data.items():
        add_method(server,key,value)  

    while True:
        print(server.recv(2048))
        server.send(bytes("recieved",'utf-8'))