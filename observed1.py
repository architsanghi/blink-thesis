import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time
import math

min_packet_threshold= 8 
threshold_min_packets=5

parser = argparse.ArgumentParser()
parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


args = parser.parse_args()
duration= args.duration

start_time= time.time()
pid_list = []

prev_list_normal=[]
current_list_normal=[]

iteration_number=0

f= open('attack.txt','w')

file_chisq= open('chi-sq-results.txt','w')

file_expected= open('probab1.txt','r')

expected_lines= file_expected.readlines()

probab_dict= dict()

for line in expected_lines:
	current_array= line.split(" ")
	if float(current_array[1]) > 0.0:
		probab_dict[int(current_array[0])]= float(current_array[1])
	

for key in probab_dict.keys():
	print(key,probab_dict[key])




g=0
window_count= -1

time.sleep(10)

while True:
	window_count= window_count + 1
	time.sleep(5)
	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	p1.wait()

	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	p2.wait()

	myfile1=open("out1.txt","r")
	count1=0
	line1 = myfile1.readlines()
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

	if iteration_number==0:
		packets_seen=0
		normal_list=[]
		for i in probab_dict.keys():
			normal_list.append(i)
		#calculate current window distribution.
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i in my_reg3:
			temp_count= i[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])
		
	else:
		packets_seen=0
		normal_list=[]
		# print(temp3)
		for i in probab_dict.keys():
			normal_list.append(i)
		#calculate current window distribution.
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i,j in zip(my_reg3,prev_list):
			temp_count= i[1]-j[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])


		
	if packets_seen==0:
		break
		#perform chi square with normal


	normal_only_list= [x for x in normal_list if x not in actual_list]
	actual_only_list= [x for x in actual_list if x not in normal_list]
	nrml_atck_int= set(normal_list).intersection(actual_list)
	print("intersection lenght is ",len(nrml_atck_int))

	# print("normaly only list is", len(normal_only_list),normal_only_list)

	print("actual only list is", actual_only_list)
	

	# print(normal_list)

	# print(actual_list)

	#chi square test
	chi_sq_normal=0

	for i in nrml_atck_int:
		observed_value= float(actual_bl_code[i])
		expected_value= (float(packets_seen)*probab_dict[i])
		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		val_to_add= squared_val/expected_value
		print(i,observed_value,expected_value,probab_dict[i],val_to_add)
		# chi_sq_normal= chi_sq_normal + val_to_add
		if expected_value < min_packet_threshold and observed_value < min_packet_threshold:
			e=0
		else:
			chi_sq_normal=chi_sq_normal+val_to_add

	for i in normal_only_list:
		observed_value= 0
		expected_value= (float(packets_seen)*probab_dict[i])
		if expected_value > 0:
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			print(i,observed_value,expected_value,probab_dict[i],val_to_add)
			
		chi_sq_normal= chi_sq_normal + val_to_add
		
		

	for i in actual_only_list:
		observed_value= actual_bl_code[i]
		expected_value= threshold_min_packets
		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		val_to_add= squared_val/expected_value
		if observed_value < min_packet_threshold and expected_value < min_packet_threshold:
			e=0
		else:
			chi_sq_normal=chi_sq_normal+val_to_add

		


	union_val= len(normal_list)+len(actual_list)-len(nrml_atck_int)
	if union_val>0:
		print("################ Normal chi square ################ ")
		print("Window: ",window_count)
		print(chi_sq_normal,union_val,packets_seen)


	# printing_message= "Chi square results"
	# message_to_write= "Chi square results" + str(line_number) + "," str(chi_sq_normal) + "," + str(union_val)
	# file_chisq.write("chi square results--> ")
	# file_chisq.write("Current window is ")
	# file_chisq.write(str(window_count))
	# file_chisq.write(" ")
	# file_chisq.write("Value for chi square is ")
	# file_chisq.write(str(chi_sq_normal))
	# file_chisq.write(" ")
	# file_chisq.write("Total number of equivalence classes ")
	# file_chisq.write(str(union_val))
	# file_chisq.write("\n")
	# f.write("%s,", message_to_write)
	

	
	# for item in curr_window:
	# 	to_write1= str(item[0])
	# 	to_write2= str(item[1])
		# f.write("%s," %to_write1)
		# f.write("%s," %to_write2)



		#perform chi sqaure test ((o-e)^2)/e
		#write in a file the chi value.
	# f.write("\n")
	prev_list=my_reg3
	iteration_number=iteration_number+1
	print("\n")

for pid in pid_list:
    pid.wait()

