# -*- coding: utf-8 -*-
#milad teimouri
#91522059


from socket import *
from time import *
from threading import *
from random import *
import sys

server_addr=gethostname()
server_port=10000

client_socket=socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_addr,server_port))


client_socket.settimeout(None)


global count
global now_count
#global file_name
#global pass_name
global fileName
count=0


def receive():
	global count,now_count
	while 1:
		#print "i am listining in top recv func"
		response2=client_socket.recv(1024)
		print "in receive func receive ",response2
		if response2[0:12]=="StreamReq#OK":
			to_send=response2[13:]
			#print "to send is : ",to_send
			to_send=to_send.split("#")
			UDP_socket = socket(AF_INET,SOCK_DGRAM)
			UDP_socket.settimeout(None)
			f=open('/home/milad/Public/course/socket/'+fileName,'r')
			#print "i am top of chunk file and f = ",f
			#chunk=""
			while 1:
				#print "!!!!!!"
				chunk=f.read(10*1024)
				if not chunk:
					#print "1)i wanna send end of file"
					
					UDP_socket.sendto("!*9(endOfTiH3*!FiL3!!!",(to_send[0],int(to_send[1])))
					print "end of file read"
					break
				#print "1)chun k = ",chunk,"wanna send to  ",to_send[1]
				ntime=time()
				UDP_socket.sendto(chunk,(to_send[0],int(to_send[1])))
				temp=(time()-ntime)
				speed=len(chunk)/(temp*1000000)
				print "chunk send by speed ",speed," Mbps"
				#print "2)chun k = ",chunk,"send to ",to_send[1]



		elif response2[0:10]=="StreamReq#" :
			ack=raw_input("do you wanna file with name "+response2[10:]+"? : ")
			if ack=="yes":
				UDP_socket4recv = socket(AF_INET,SOCK_DGRAM)
				UDP_socket4recv.settimeout(None)
				UDP_socket4recv.sendto("alaki",('',3333))
				port_number=UDP_socket4recv.getsockname()

				#UDP_socket4recv.bind(UDP_socket4recv.getsockname())
				client_socket.send("StreamReq#OK#"+server_addr+"#"+str(port_number[1]) )
				print "UDP socket is listining "
				#start_time=time()
				#count=count+1
				count=random()
				#print "count is ",count
				fileName_=response2[10:]
				file_name=fileName_.split(".")[0]
				pass_name=fileName_.split(".")[1]
				
				myFile = open('/home/milad/Public/course/socket/'+file_name+str(count)+"."+pass_name, 'wb')

				while 1:
					ntime=time()
					chunk2=UDP_socket4recv.recvfrom(10*1024)
					temp=(time()-ntime)
					speed=len(chunk2[0])/(temp*1000000)
					print "chunk receive by speed ",speed," Mbps"
					#print "chunk2 is ",chunk2,"and type ",type(chunk2)
					if (chunk2[0] == "!*9(endOfTiH3*!FiL3!!!"):
						print "it will break :|"
						break

					myFile.write(chunk2[0])
				myFile.close()
				now_count=count
				#data=UDP_socket4recv.recvfrom(10240)

				print "data receive"
				#print data[0]


			else:
				client_socket.send("StreamReq#NOK" )
		elif response2[0:7]=="Stream#":
			print "i am in send =>",response2
			to_send2=response2[7:]
			to_send2=to_send2.split("#")
			print to_send2
			UDP_socket2 = socket(AF_INET,SOCK_DGRAM)
			UDP_socket2.settimeout(None)
			print "now count is ",now_count
			
			f=open('/home/milad/Public/course/socket/'+file_name+str(now_count)+"."+pass_name,'r')
			while 1:
				#print "####################"
				chunk=f.read(10*1024)
				if not chunk:
					#print "i wanna send last part"
					UDP_socket2.sendto("!*9(endOfTiH3*!FiL3!!!",(to_send2[0],int(to_send2[1])))
					break
				ntime=time()
				UDP_socket2.sendto(chunk,(to_send2[0],int(to_send2[1])))
				temp=(time()-ntime)
				speed=len(chunk)/(temp*1000000)
				print "chunk send by speed ",speed," Mbps"
			print "data sent p2p "
		elif response2[0:8]=="Reg#NOK#":
			print "Error : ",response2[8:]


			


#t1 = Thread(target=receive, args=[])
t1 = Thread(target=receive , args=())
t1.daemon = True


while 1:
	name=raw_input("pick up a name for your host : ")
	client_socket.send("Reg#"+name)
	response=client_socket.recv(1024)
	#print response
	if response == "‫Reg#OK":
		print "registered !"
		break
	else :
		print "your name is repeated !"
#print "now t2 will start"
t1.start()
#print "!!!!"
while 1:
	command=raw_input("enter your command : ")
	if command[0:10]=="StreamReq#":
		fileName=command[10:]
		file_name=fileName.split(".")[0]
		pass_name=fileName.split(".")[1]

	client_socket.send(command)
	if command=="Bye":
		client_socket.close()
		print "connection closed !"
		sys.exit()
	#response=client_socket.recv(1024)
	#print "here response must showen = ",response
	







#send_()

#print "i am out of while"
#client_socket.close()