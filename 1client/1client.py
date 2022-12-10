import socket
import platform
import threading
import os 
import datetime 
import pytz
from pathlib import Path

clientname = 'CLIENT1'


def add_method(server,key,data):
    dat = f"ADD {key} P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\nTitle: {data}\n\n"
    print(f"sent{dat}")
    server.send(bytes(dat,'utf-8'))

def list_method(server):
    dat = f"LIST ALL P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\n\n"
    server.send(bytes(dat,'utf-8'))

def lookup_method(server,key):
    dat = f"LOOKUP {key} P2P-CI/1.0\nHost: {clientname}\nPort: {p2psockname}\n\n"
    server.send(bytes(dat,'utf-8'))

def request(key,port,server):
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.connect((socket.gethostname(), port))
    o_s=platform.system()
    dat = f"GET {key} P2P-CI/1.0\nHost: {clientname}\nOS: {o_s}\n\n"
    ss.send(bytes(dat,'utf-8')) 
    temp = ss.recv(16048, socket.MSG_PEEK)
    length = temp.find(b'\n\n')
    msg=str(ss.recv(length+2),encoding='utf-8')
    lines=msg.split('\n')
    if(lines[0]=="404 Not Found"):
        print(msg)
    elif(lines[0][0:3]=="400 Bad Request"):
        print(msg)
    elif(lines[0][0:3]=="505 P2P-CI Version Not Supported"):
        print(msg)
    else:
        l1=lines[1]
        l1=lines[0].split(" ")
        rfcnum = l1[3]
        rfctitle=lines[1][5:]
        print(lines)
        l5=lines[5]
        with open(f"./1client/{rfcnum} {rfctitle}", 'w') as f:
            f.write(l5)
        add_method(server,rfcnum,rfctitle)

def GET(msg):
    lines=msg.split('\n')
    l1=lines[0].split(" ")
    return l1[1],l1[2]

def response(cs,ip):
    # print(cs)
    client_port = None
    client_port=str(cs.getpeername()[1])
    
    p2p_file=''
    c=0
    while True:
        temp = cs.recv(2048, socket.MSG_PEEK)
        length = temp.find(b'\n\n')
        msg=str(cs.recv(length+2),encoding='utf-8')
        # print(msg)
        if msg[:2] == 'GE':
            rfcreq,version = GET(msg)
            list_of_files = os.listdir("./1client") 
            if(str.isnumeric(rfcreq)==False):
                data="400 Bad Request\n\n"
            elif(version!='P2P-CI/1.0'):
                data="505 P2P-CI Version Not Supported\n\n"
            else:
                for each_file in list_of_files:
                    if each_file.startswith(str(rfcreq)):  
                        c=c+1
                        p2p_file=each_file
                if(c==0):
                    data="404 Not Found\n\n"
                else:
                    current_data_time=datetime.datetime.now(pytz.timezone('America/New_York'))
                    o_s=platform.system()
                    with open(f'./1client/{p2p_file}',"r") as f: 
                        content_length=len(f.readlines())
                    txt = Path(f'./1client/{p2p_file}').read_text()
                    txt=txt.replace('\n', ' ')
                    p2p_reponse=f"P2P-CI/1.0 200 OK {rfcreq}\n{p2p_file}\nDate: {current_data_time}\nOS: {o_s}\nContent-Length: {content_length}\nContent-Type: Text/Text\n{txt}\n\n"
                    data = p2p_reponse   
            cs.send(bytes(data,'utf-8'))
            cs.close()
            return
        else:
            cs.send(bytes("400 Bad Request",'utf-8'))
            cs.close()
            return



if __name__=='__main__':
    data = {}
    for x in os.listdir("./1client"):
        print(x)
        if x.endswith('.txt'):
            x=x[:len(x)-4]
            data[x[0:4]]=x[5:]
    print(data)
    p2p = socket.socket()
    clientip=socket.gethostbyname(socket.gethostname())
    p2p.bind((clientip,0))
    p2psockname = p2p.getsockname()[1]
    p2p.listen(5)

    def ptop():
        while True:
            # print('Server listening')
            cs,ip=p2p.accept()
            # connect_new_client,(cs,ip)
            threading._start_new_thread(response,(cs,ip))

    def ptos():
        global data
        print(f"{data}")
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.connect((socket.gethostname(), 7734))
        print(f'Connted to server {server.getsockname()} {server.getpeername()}')
        for key,value in data.items():
            add_method(server,key,value)  
        while True:
            a = int(input('Enter Lookup(1)/List(2)/Get(3):'))
            if a == 1:
                key = input('Enter RFC number to search:')
                lookup_method(server,key)
                print(data:=server.recv(2048))
            elif a==2:
                list_method(server)
                print(data:=server.recv(2048))
            elif a==3:
                key=input("Enter RFC file to recieve:")
                if len(key)==4:
                    clientport=int(input("Enter Client port to request transfer:"))
                    request(key,clientport,server)
                else:
                    print("400 Bad Request")
            else:
                print("400 Bad Request")

    t1 = threading.Thread(target =ptop)
    t2 = threading.Thread(target =ptos)
    t1.start()
    t2.start()    
            


