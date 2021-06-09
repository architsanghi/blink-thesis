from scapy.all import *
pkt_list= rdpcap("./pcap/s1-eth1_out.pcap")



# pkt_list[2]=pkt_list[3]

# print(pkt_list[2].show())
# print("\n")
# print(pkt_list[3].show())
# # print(pkt_list[2].sequence)
# if pkt_list[2]==pkt_list[3]:
# 	print("yes")
# else:
# 	print("no")




# for i in pkt_list:
# 	i.show()
# print(len(pkt_list))

print(len(pkt_list))
wrpcap("modified.pcap",pkt_list)