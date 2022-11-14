import socket
import threading
import json
import datetime
import subprocess
import time
import os
import re

with open('server.json') as f:
    server1 = json.load(f)

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

with open('cmdlist.json')as f_cmdlist:
    cmdlist = json.load(f_cmdlist)

host = "127.0.0.1"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
print("Server is ready...")
clients = {}
serverRunning = True

def handle_client(conn, uname):
    clientConnected = True
    keys = clients.keys()

    while clientConnected:
        try:
            response = '[SERVER] Number of People Online\n'
            response1 = '[SERVER] Command list\n'
            data = conn.recv(1024).decode('ascii')
            message_s = re.findall(r'\[.*?\]', data)[0]
            data_out = data.replace(f'{message_s}', '')
            found = False
            if '@' in data:
                for name in list(clients):
                    if('@'+name) in data:
                        print('hi')
                        data = data.replace('@'+name,'')
                        clients.get(name).send(data.encode('ascii'))
                        found = True
            elif '/' not in data:
                conn.send(data.encode('ascii'))
                for k,v in clients.items():
                    if v != conn:
                        v.send(data.encode('ascii'))
                        found = True
            elif '/list' in data:
                clientNo = 0
                for name in list(clients):
                    clientNo += 1
                    response = response + str(clientNo) +'::' + name+'\n'
                conn.send(data.encode('ascii'))
                conn.send(response.encode('ascii'))
                found = True
            elif data_out == '/help':
                cmdNo = 0
                for cmdlist1 in list(cmdlist):
                    cmdNo += 1
                    response1 = response1 + str(cmdNo) +'::' + cmdlist1+ '::' + cmdlist.get(cmdlist1) + '\n'
                conn.send(data.encode('ascii'))
                conn.send(response1.encode('ascii'))
                found = True

            else:
                if '/' in data:
                    data = data.replace('/', '')
                    if os.path.exists(f'commands\\{data_out}.ini'):
                        with open(f'commands\\{data_out}.ini')as f_cmd:
                            cmd = f_cmd.read()
                        cmd = f"//{uname}//" + cmd.replace('\n', ';')
                        conn.send(cmd.encode('ascii'))
                    else:
                        conn.send("[SERVER-ERROR] could not execute command. please enter a valid command or use '/help' to list all the commands".encode())
                    found = True
                conn.send(data.encode('ascii'))
                if(not found):
                    conn.send('[SERVER] Trying to send message to invalid person.'.encode('ascii'))
            print(get_color_escape(21, 170, 13)+str(message_s),get_color_escape(255, 255, 255),data_out)

        except Exception as e:
            try:
                del clients[uname]
            except:
                False
            print(e)
            print(f"{get_color_escape(21, 170, 13)}[SERVER]{get_color_escape(255, 255, 255)} {uname} has logged out")
            clientConnected = False


def kick_cli():
    while 1:
        try:
            in_data = input()
            response = '[SERVER] Number of People Online\n'
            found = False
            if '/' not in in_data:
                for k,v in clients.items():
                    if v != conn:
                        print(in_data)
                        found = True
            elif '/list' in in_data:
                clientNo = 0
                for name in list(clients):
                    clientNo += 1
                    response = response + str(clientNo) +'::' + name+'\n'
                print(response)
                found = True
                
            else:
                for name in list(clients):
                    if(f'/kick {name}') in in_data:
                        clients.get(name).send(f'43896jfr2j36ru93fruyj63u9kfr39>{name}<em8jy42oriy2ofrju3oru37u3j'.encode('ascii'))
                        del clients[name]
                        found = True
                    elif '/' in in_data:
                        in_data = in_data.replace('/', '')
                        if os.path.exists(f'commands\\{in_data}.ini'):
                            with open(f'commands\\{in_data}.ini')as f_cmd:
                                cmd = f_cmd.read()
                            exec(cmd)
                        found = True
                if(not found):
                    print('[SERVER] Trying to send message to invalid person.'.encode('ascii'))
        except:
            clientConnected = False


while serverRunning:
    try:
        conn,addr = s.accept()
        idf = conn.recv(1024).decode('ascii')
        if idf == '389237489264738728402938242':
            uname = conn.recv(1024).decode('ascii')
            print(f"{get_color_escape(21, 170, 13)}[SERVER]{get_color_escape(255, 255, 255)} {uname} joined")
            conn.send(f"Welcome to {server1['name']}. Type //help to know all the commands".encode('ascii'))
            if(conn not in clients):
                clients[uname] = conn
                threading.Thread(target = handle_client, args = (conn, uname,)).start()
                threading.Thread(target=kick_cli).start()
        else:
            conn.send('Unsupported client version. Please use something like UpBox-2.0.8 or higher'.encode('ascii'))

    except:
        clientConnected = False
s.close()