import socket
from threading import Thread
import json
import datetime
from colorama import Fore
import subprocess

subprocess.call('cls', shell=True)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5006
separator_token = ": "

with open('server.json') as f:
    server1 = json.load(f)

with open('server.json') as ff:
    server2 = ff.read()
ch1 = u'\u2713'

if server1['colors'][0]['color'] == 'green':
    print(Fore.GREEN)
elif server1['colors'][0]['color'] == 'blue':
    print(Fore.BLUE)
elif server1['colors'][0]['color'] == 'red':
    print(Fore.RED)

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            print(msg)
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
                    cs.send(f'//{cmd_name}[!] Command does not exist'.encode())

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
    print(f"[+] {client_address} Connected as {c_name}")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
    print(f"[{ch1}] {client_address} Verified as {c_name}")
for cs in client_sockets:
    cs.close()
s.close()