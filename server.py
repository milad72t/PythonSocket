# -*- coding: utf-8 -*-
#milad teimouri
#91522059

from socket import *
from threading import *
from time import *


server_port=10000

global server_socket
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(3)
server_socket.settimeout(None)
global name_clients
global addr_clients
global sock_clients
global count
global clinet_want
global UDP_clinets
global applicant
name_clients = []
sock_clients = []
addr_clients =[]
clinet_want=[]
UDP_clinets=[]
def func(connection_socket,address) :
	global name_clients , sock_clients,server_socket,addr_clients,count,clinet_want,UDP_clinets,applicant
	while 1:
		message = connection_socket.recv(1024)
		print message , address
		if message[0:4] == "Reg#":
			#print "i am in 1"
			flag = register(connection_socket,message,address)
			if flag==1:
				break
			else:
				print "try again"
			
		else:
			print "you must first register"
	while 1:
		message1 = connection_socket.recv(1024)
		#print "message1 is ",message1
		if message1[0:10]=="StreamReq#" and message1[10:12]!="OK" and message1[10:12]!="NO":
			#print "i am in stream if"
			clinet_want=[]
			UDP_clinets=[]
			stream_name=message1[10:]
			applicant=connection_socket


			hh=0
			#print "counet is zero !!!"
			count=0
			for sock_i in sock_clients:
				#print "i am in hh=",hh
				if (addr_clients[sock_clients.index(sock_i)]==address):
					continue
				
				hh = hh+1
				sock_i.send(message1)
				print "i send message tou ",name_clients[sock_clients.index(sock_i)]

				######################
		elif message1[0:10]=="StreamReq#" and (message1[10:12]=="OK" or message1[10:12]=="NO"):		
			#print "i am in elif special func"
			
				#response1=sock_i.recv(1024)
			count=count+1
			#print "i receive something and count is",count
			print "2)message1 is",message1
			if message1[0:12]=="StreamReq#OK":
				print name_clients[sock_clients.index(connection_socket)],"accept file :D"
				clinet_want.append(connection_socket)
				UDP_clinets.append(message1[13:])
				print UDP_clinets

			elif message1=="StreamReq#NOK":
					print name_clients[sock_clients.index(connection_socket)],"reject file :("
			if (len(sock_clients)-1)==count:			
				
				if len(clinet_want)>0:		
					#print "ferestadam be darkhast konande"
					applicant.send("StreamReq#OK#"+(UDP_clinets[0]))
				#print "len(clients) = ",len(clinet_want)
				#print "len(UDP) = ",len(UDP_clinets)
				for i in range(len(clinet_want)-1):
					print "req for send to ",name_clients[sock_clients.index(clinet_want[i])],"for recv ",name_clients[sock_clients.index(clinet_want[i+1])]
					sleep(1)
					clinet_want[i].send("Stream#"+(UDP_clinets[i+1]))
			
		elif message1=="Bye":
			try :
				name_rem=name_clients[sock_clients.index(connection_socket)]
				addr_rem=addr_clients[sock_clients.index(connection_socket)]
				sock_clients.remove(connection_socket)
				name_clients.remove(name_rem)
				addr_clients.remove(addr_rem)
				#connection_socket.send("Bye#OK")
				print name_rem,"logout from chain :("
				#connection_socket.close()
			except:


				connection_socket.send("Bye#NOK")
		elif message1[0:4]=="Reg#":
			connection_socket.send("Reg#NOK#alreadyexit")



def register(sock,msg,addr):
	global name_clients , sock_clients,addr_clients
	#print "i am in register function by message = ",msg
	
	c_name=msg[4:]
	if c_name in name_clients:
		#print "i am in if stat"
		sock.send("‫Reg#NOK#RepeatedName‬‬")
		return 0
	else:
		print c_name,"successfully login "
		sock.send("‫Reg#OK")
		name_clients.append(c_name)
		sock_clients.append(sock)
		addr_clients.append(addr)
		return 1





while True:
	connection_socket_ , address_ = server_socket.accept()
	connection_socket_.settimeout(None)
	Thread(target=func, args=(connection_socket_,address_,)).start()

