import socket
import platform
import threading
import os


clientname = 'ajay'
data = {
        '0791':'Internet Protocol',
        '0792':'Internet Control Message Protocol'
    }

def add_method(server,key,data):
    dat = f"ADD {key} P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\nTitle: {value}\n\n"
    server.send(bytes(dat,'utf-8'))

def list_method(server):
    dat = f"LIST ALL P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\n\n"
    server.send(bytes(dat,'utf-8'))

def lookup_method(server,key):
    dat = f"LOOKUP {key} P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\n\n"
    server.send(bytes(dat,'utf-8'))

def request(key,port,server):
    host=socket.gethostname()
    ss=socket.socket()
    ss.bind((host,port))
    ss.listen(2)
    conn, address = ss.accept()  
    os=platform.system()
    dat = f"GET {key} P2P-CI/1.0\nHost: {clientname}\nOS: {os}\n\n"
    conn.send(bytes(dat,'utf-8')) 
    #read the response from conn as conn.recv
    #parse the response to make sense
    # recieved data = conn.recv(2048)

    #server.send(add_method(x,y,z))

def GET(msg):
    #parse RFC number and return
    pass

def response(cs,ip):
    print(cs)
    client_port = None
    client_port=str(cs.getpeername()[1]-1)
    try:
        while True:
            # cs.send(bytes(input('Enter msg:'),'utf-8'))
            temp = cs.recv(2048, socket.MSG_PEEK)
            length = temp.find(b'\n\n')
            msg=str(cs.recv(length+2),encoding='utf-8')
            print(msg)
            if msg[:2] == 'GE':
                rfcreq = GET(msg)
                # process rfcreq formatt it as data
                # read rfcreqnum from data and read filenames as = rfcreq+'-'+data[rfcreq]+'.txt'
                data = 'Formatted response'
                cs.send(bytes(data,'utf-8'))
            else:
                # Bad request response and other methods
                pass
        
    except(ConnectionError or ConnectionResetError or ConnectionAbortedError):
        print(f'\n\n\nError client {client_port}\n\n\n')
        cs.close()



if __name__=='__main__':

    data = {}
    for x in os.listdir():
        if x.endswith('.txt'):
            #parse the filenames into dictionary
            #filenames: 0791-Internet Protocols.txt,.....
            pass

    p2p = socket.socket()
    clientip=socket.gethostbyname(socket.gethostname())
    p2p.bind((clientip,0))
    p2psockname = p2p.getsockname()[1]
    p2p.listen(5)

    def ptop():
        while True:
            print('Server listening')
            cs,ip=p2p.accept()
            # connect_new_client,(cs,ip)
            threading._start_new_thread(response(cs,ip))

    def ptos():
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.connect((socket.gethostname(), 7734))
        print(f'Connted to server {server.getsockname()} {server.getpeername()}')
        for key,value in data.items():
            add_method(server,key,value)  
        while True:
            server.send(bytes("recieved",'utf-8'))
            temp = server.recv(2048, socket.MSG_PEEK)
            length = temp.find(b'\n\n')
            msg=str(server.recv(length+2),encoding='utf-8')

            a = int(input('Enter Lookup(1)/List(2)/Get(3):'))
            if a == 1:
                key = input('Enter RFC number to search:')
                lookup_method(server,key)
                print(data:=server.recv(2048))
            elif a==2:
                list_method(server)
                print(data:=server.recv(2048))
            elif a==3:
                key=input("Enter RFC file to send:")
                clientport=input("Enter Client port to request transfer")
                #call request function(server,clientport,rfcnum)

    t1 = threading.Thread(target =ptop)
    t2 = threading.Thread(target =ptos)
    t1.start()
    t2.start()    
            


