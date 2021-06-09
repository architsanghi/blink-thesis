import socket
import struct
import time
import subprocess, os , signal
Duration=30

f= open("/home/p4/Blink/attack-time.txt",'w')
# f.write("hello")
# f.close()


def send_msg(sock, msg):

    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def expected_traffic(startTime,totalTime,s):
	while (time.time() - startTime <= totalTime):
		send_msg(s,"hello")
       	i +=1
        next_send_time = startTime + i * ipd *1
        time.sleep(max(0,next_send_time - time.time()))
# def observed_traffic(start_time_attack,totalTime,s):
# 	count=0
# 	start_time_attack = 0
# 	end_time_attack = 0
# 	while (time.time() - startTime <= totalTime):
# 		if time.time()-startTime<=0.50*totalTime:
# 			s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
#         	send_msg(s,"hello")
#         elif time.time()-startTime<= 0.75*totalTime:
#         	count= 1-count
#         	if count==0:
#         		s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
#         		send_msg(s,"hello")
#         	else:
#         		s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
#         		send_msg(s,"hello") 
#         else:
#         	if end_time_attack==0:
#         		f.write(str(time.time()-startTime-5))
# 				end_time_attack=1
# 				s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
# 				send_msg(s,"hello")
# 		i +=1
#         next_send_time = startTime + i * ipd
#         time.sleep(max(0,next_send_time - time.time()))


def sendFlowTCP(dst="10.0.32.3",sport=5000,dport=5001,ipd=1,duration=0):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG, 1500)

    s.bind(('', sport))

    try:
        reconnections = 5
        while reconnections:
            try:
                s.connect((dst, dport))
                break
            except:
                reconnections -=1
                print "TCP flow client could not connect with server... Reconnections left {0} ...".format(reconnections)
                time.sleep(0.5)

        #could not connect to the server
        if reconnections == 0:
            return

        totalTime = int(duration)
        startTime = time.time()
        i = 0
        time_step = 1	


        # expected_traffic(startTime,totalTime,s)
       
        normal traffic
       	count=0
        while (time.time() - startTime <= totalTime):
            send_msg(s,"hello")
            i +=1
            next_send_time = startTime + i * ipd *1
            time.sleep(max(0,next_send_time - time.time()))

        # burst attack 
        # while (time.time() - startTime <= totalTime):
        #     send_msg(s,"hello")
        #     i +=1
        #     next_send_time = startTime + i * ipd *0.0001
        #     time.sleep(max(0,next_send_time - time.time()))


        # CASE 1 taking backup1 link
        # count=0
        # while (time.time() - startTime <= totalTime):
        #     if time.time()-startTime<=0.50*totalTime:
        #     	s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=1*totalTime:
        #     	count= 1-count
        #     	if count==0:
        #     		s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #     		send_msg(s,"hello")
        #     	else:
        #     		s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #     		send_msg(s,"hello") 
        #     else:
        #     	s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")

        #     i +=1
        #     next_send_time = startTime + i * ipd
        #     time.sleep(max(0,next_send_time - time.time()))


        # BACKUP LINK 1 try

        # count=0
        # start_time_attack=0
        # end_time_attack=0
        # while (time.time() - startTime <= totalTime):
        #     if time.time()-startTime<=0.50*totalTime:
        #     	s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<= 0.75*totalTime:
        #     	count= 1-count
        #     	if count==0:
        #     		s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #     		send_msg(s,"hello")
        #     	else:
        #     		s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #     		send_msg(s,"hello") 
        #     else:
        #     	if end_time_attack==0:
        #     		f.write(str(time.time()-startTime-5))
        #     		end_time_attack=1
        #     	s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")

        #     i +=1
        #     next_send_time = startTime + i * ipd
        #     time.sleep(max(0,next_send_time - time.time()))




























        # CASE 2 taking backup2 link try
        # while (time.time() - startTime <= totalTime):
            
        #     if time.time()-startTime<=0.25*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.40*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.60*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.80*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #         send_msg(s,"hello")
        #     else:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")

        #     i +=1
        #     next_send_time = startTime + i * ipd
        #     time.sleep(max(0,next_send_time - time.time()))



        # CASE 3 retransmissions at beginning
        # while (time.time() - startTime <= totalTime):
            
        #     if time.time()-startTime<=0.20*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.40*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.60*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,12)
        #         send_msg(s,"hello")
        #     elif time.time()-startTime<=0.80*totalTime:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,2)
        #         send_msg(s,"hello")
        #     else:
        #         s.setsockopt(socket.SOL_IP,socket.IP_TTL,10)
        #         send_msg(s,"hello")

        #     i +=1
        #     next_send_time = startTime + i * ipd
        #     time.sleep(max(0,next_send_time - time.time()))

    except socket.error:
        pass

    finally:
        s.close()

#normal recieve flow 
def recvFlowTCP(dport=5001,**kwargs):

    """
    Lisitens on port dport until a client connects sends data and closes the connection. All the received
    data is thrown for optimization purposes.
    :param dport:
    :return:
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    s.bind(("", dport))
    s.listen(1)
    conn = ''
    buffer = bytearray(4096)
    try:
        conn, addr = s.accept()
        while True:
            #data = recv_msg(conn)#conn.recv(1024)
            if not conn.recv_into(buffer,4096):
                break

    finally:
        if conn:
            conn.close()
        else:
            s.close()

#attack recv flow 
# def recvFlowTCP(dport=5001,**kwargs):

#     """
#     Lisitens on port dport until a client connects sends data and closes the connection. All the received
#     data is thrown for optimization purposes.
#     :param dport:
#     :return:
#     """

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

#     s.bind(("", dport))
#     s.listen(1)
#     conn = ''
#     buffer = bytearray(4096)
#     startTime_rec= time.time()
#     try:
#         conn, addr = s.accept()
#         while (time.time() - startTime_rec <= Duration):
#             if time.time()-startTime_rec <= 0.15*Duration:
#                 if not conn.recv_into(buffer,0):
#                     break
#             elif time.time()-startTime_rec<=0.20*Duration:
#                 conn.recv_into(buffer,4096)
#                 stub_code= 'my_Stub'
#             else:
#                 stub_code='my_Stub'
#                 if not conn.recv_into(buffer,4096):
#                     break

#     finally:
#         if conn:
#             conn.close()
#         else:
#             s.close()

# def recvFlowTCP(dport=5001,**kwargs):

#     """
#     Lisitens on port dport until a client connects sends data and closes the connection. All the received
#     data is thrown for optimization purposes.
#     :param dport:
#     :return:
#     """

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

#     s.bind(("", dport))
#     s.listen(1)
#     conn = ''
#     startTime_rec= time.time()
#     buffer = bytearray(4096)
#     try:
#         conn, addr = s.accept()
#         while time.time()-startTime_rec<= Duration :
#             if time.time()-startTime_rec<= 0.2*Duration:
#                 conn.recv(1)
#             else:
#                 conn.recv(1024)

#     finally:
#         if conn:
#             conn.close()
#         else:
#             s.close()

