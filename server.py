import socket
import threading
from pprint import pprint as pp

PORT=7734
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)

client_mapping={}   #portnumber:clientname
rfc_mapping={}      #rfcnumber:[title,[list of clientname]]


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

def ADD(msg):
    lines=msg.split('\n')
    l1=lines[0].split(" ")
    l2=lines[1].split(" ")
    l3=lines[2].split(" ")
    l4=lines[3]
    rfcnum = l1[1]
    rfcver = l1[2]
    clientname = l2[1]
    portnumber=l3[1]
    title=l4[7:]
    
    client_mapping[portnumber]=clientname
    if rfcnum in rfc_mapping.keys():
        #Skipping version checking
        rfc_mapping[rfcnum][1].append(clientname)
    else:
        #No duplication check for client name
        rfc_mapping[rfcnum] = [title, [clientname]]

def LOOKUP(msg):
    lines=msg.split('\n')
    l1=lines[0].split(" ")
    rfcnum = l1[1]
    return rfcnum


def connect_new_client(cs,ip):
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
            if msg[:2] == 'AD':
                ADD(msg)
                pp(client_mapping)
                print('\n')
                pp(rfc_mapping)
            elif msg[:2] == 'LO':
                rfc = LOOKUP(msg)
                if rfc in rfc_mapping:
                    cs.send(bytes(str(rfc_mapping[rfc]),'utf-8'))
                else:
                    cs.send(bytes('Error RFC not found','utf-8'))
                pass
            elif msg[:2] == 'LI':
                cs.send(bytes(str(rfc_mapping),'utf-8'))
                pass
        
    except(ConnectionError or ConnectionResetError or ConnectionAbortedError):
        print(f'\n\n\nError client {client_port}\n\n\n')
        if client_port == None:
            print('Cant get client port')
            return
        clientname = client_mapping.pop(client_port)
        obsoleterfcs = []
        for key,value in rfc_mapping.items():
            if clientname in value[1]:
                if(len(value[1])>1):
                    value[1].remove(clientname)
                else:
                    obsoleterfcs.append(key)
        for rfc in obsoleterfcs:
            rfc_mapping.pop(rfc)
        pp(client_mapping)
        print('\n')
        pp(rfc_mapping)
        cs.close()

while True:
    print('Server listening')
    cs,ip=server.accept()
    # connect_new_client,(cs,ip)
    threading._start_new_thread(connect_new_client(cs,ip))


def handle_client(conn,addr):
    pass

def start():
    pass    