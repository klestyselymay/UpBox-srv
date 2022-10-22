import socket
from threading import Thread
import json
import datetime
from colorama import Fore
import subprocess
import time
import re

subprocess.call('cls', shell=True)

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5006

with open('server.json') as f:
    server1 = json.load(f)

with open('server.json') as ff:
    server2 = ff.read()

client_sockets = set()
s = socket.socket()
print(f"{get_color_escape(21, 170, 13)}[SERVER]{Fore.WHITE} Successfully created socket")
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
time.sleep(.6)
s.bind((SERVER_HOST, SERVER_PORT))
print(f"{get_color_escape(21, 170, 13)}[SERVER]{Fore.WHITE} Successfully created bind")
time.sleep(.6)
s.listen(5)
print(f"{get_color_escape(21, 170, 13)}[SERVER]{Fore.WHITE} Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            message = msg
            message_s = re.findall(r'\[.*?\]', message)
            message = message.replace(f'{message_s[0]} ', '')
            print(get_color_escape(21, 170, 13)+message_s[0],Fore.WHITE,message)
            if '//' in msg:
                cmd = msg
                cmd = cmd.split('=')
                cmd_name = cmd[0].replace('//', '')
                cmd = cmd[1]
                if cmd in server2:
                    cmd_out = server1['commands'][0][cmd]
                    cmd_out = '/'+cmd_name+'/'+cmd_out
                    cs.send(cmd_out.encode())
                else:
                    cs.send(f'//{cmd_name}[SERVER] Command does not exist'.encode())

        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            dsfsk = True
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address = s.accept()
    c_name = client_socket.recv(1024).decode()
    print(f"{get_color_escape(21, 170, 13)}[SERVER]{Fore.WHITE} {client_address} Connected as {c_name}")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
    print(f"{get_color_escape(21, 170, 13)}[SERVER]{Fore.WHITE} {client_address} Verified as {c_name}")
for cs in client_sockets:
    cs.close()
s.close()