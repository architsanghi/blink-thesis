import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time

parser = argparse.ArgumentParser()
parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


args = parser.parse_args()
duration= args.duration

start_time= time.time()
pid_list = []

prev_list_normal=[]
current_list_normal=[]

prev_list=[]


iteration_number=0

f= open('normal.txt','w')

lf= open('lf.txt','r')

past_list=[]

expected_lines= lf.readlines()
current_line= expected_lines[len(expected_lines)-1]
arr= current_line.split(",")
for counter in range(0,len(arr)-1,2):
	item1= float(arr[counter])
	item2=float(arr[counter+1])
	past_list.append([item1,item2])


# p1=(Popen("simple_switch_CLI --thrift-port 9090",shell=True))
# pid_list.append(p1)
# time.sleep(1)
# pid_list.append(Popen("register_read ingress.my_reg 0",shell=True))
# x= True
while True:
	time.sleep(5)
	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	p1.wait()

	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	p2.wait()

	myfile1=open("out1.txt","r")
	count1=0
	line1 = myfile1.readlines()
	# print(line)
	line_to_read1= line1[3]
	required_array1= line_to_read1[32:-1]
	temp1= required_array1.split(", ")
	my_reg1=[]
	for val in temp1:
		my_reg1.append(val)
	
	myfile1.close()


	myfile2=open("out2.txt","r")
	count2=0
	line2 = myfile2.readlines()
	# print(line)
	line_to_read2= line2[3]
	required_array2= line_to_read2[29:-1]
	temp2= required_array2.split(", ")
	my_reg2=[]
	for val in temp2:
		my_reg2.append(val)
	
	myfile2.close()

	for i in range(0,len(my_reg1)):
		my_reg1[i]= int(my_reg1[i])

	for i in range(0,len(my_reg2)):
		my_reg2[i]=int(my_reg2[i])

	my_reg3=[]
	for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
		my_reg3.append([my_reg1[i],my_reg2[j]])


	# print(my_reg3)

	curr_window=[]

	if iteration_number==0:
		for i,k in zip(my_reg3,past_list):
			temp_count= i[1]
			current_count= 0.2*temp_count + 0.8*k[1]
			if i[0]==0 and k[0]>0:
				curr_window.append([k[0],current_count])
			else:
				curr_window.append([i[0],current_count])
	else:
		for i,j,k in zip(my_reg3,prev_list,past_list):
			temp_count= i[1]-j[1]
			current_count= 0.2*temp_count + 0.8*k[1]
			if i[0]==0 and k[0]>0:
				curr_window.append([k[0],current_count])
			else:
				curr_window.append([i[0],current_count])


	

	print(len(curr_window))
	for item in curr_window:
		to_write1= str(item[0])
		to_write2= str(item[1])
		if item[1]>0:
			print(to_write1,to_write2)
		f.write("%s," %to_write1)
		f.write("%s," %to_write2)



		#perform chi sqaure test ((o-e)^2)/e
		#write in a file the chi value.
	f.write("\n")
	prev_list=my_reg3
	past_list=curr_window
	iteration_number=iteration_number+1





for pid in pid_list:
    pid.wait()

