import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import matplotlib.pyplot as plt
import time
import math
import scipy.stats


min_packet_threshold= 8 
threshold_min_packets=5

pid_list = []
iteration_number=0

file_normal= open('probab1.txt','r')
file_chi_sq= open("file_chi_sq.txt","w")
expected_normal= file_normal.readlines()
probab_normal= dict()
threshold_list_normal=[]
threshold_list_lf=[]

for line in expected_normal:
	current_array= line.split(" ")
	if float(current_array[1]) > 0.0:
		probab_normal[int(current_array[0])]= float(current_array[1])

file_link_failure= open('probab2.txt','r')
expected_link_failure= file_link_failure.readlines()
probab_link_failure= dict()

for line in expected_link_failure:
	current_array= line.split(" ")
	if float(current_array[1]) > 0.0:
		probab_link_failure[int(current_array[0])]= float(current_array[1])


normal_chi_sq_list=[]
lf_chi_sq_list=[]
save_image_to="/home/p4/Blink/images/"






time.sleep(10)

def plot_graph(x, y, xlabel, ylabel, title):
    plt.plot(x, y, 'r')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # file_last_line= count_lines[len(count_lines)-1]
    # title_name= file_last_line[0:]
    # next_file_number= int(title_name)
    # next_file_number= next_file_number + 1
    # file_count.write("\n")
    # file_count.write(str(next_file_number))
    plt.savefig(save_image_to + str(title_name + '.png'))







def chi_square_test (iteration_number, curr_dict, bl_pair_reg, prev_list, type_of_attack):
	packets_seen=0
	if iteration_number==0:
		normal_list=[]
		for i in curr_dict.keys():
			normal_list.append(i)
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i in bl_pair_reg:
			temp_count= i[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])
		
	else:
		normal_list=[]
		for i in curr_dict.keys():
			normal_list.append(i)
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i,j in zip(bl_pair_reg,prev_list):
			temp_count= i[1]-j[1]
			current_count= temp_count
			packets_seen= packets_seen + temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])


		
	if packets_seen==0:
		for i in range(len(normal_chi_sq_list)):
			file_chi_sq.write("The window Number" + str(i) + str(" ") + str(normal_chi_sq_list[i]))
			file_chi_sq.write("\n")
		for i in range(len(lf_chi_sq_list)):
			file_chi_sq.write("The window number" + str(i) + str(" ") + str(lf_chi_sq_list[i]))
			file_chi_sq.write("\n")
		return -1


	normal_only_list= [x for x in normal_list if x not in actual_list]
	actual_only_list= [x for x in actual_list if x not in normal_list]
	nrml_atck_int= set(normal_list).intersection(actual_list)
	# print("intersection lenght is ",len(nrml_atck_int))


	# print("actual only list is", actual_only_list)

	#chi square test
	chi_sq_normal=0

	for i in nrml_atck_int:
		observed_value= float(actual_bl_code[i])
		expected_value= (float(packets_seen)*curr_dict[i])
		squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		val_to_add= squared_val/expected_value
		# print(i,observed_value,expected_value,curr_dict[i],val_to_add)
		if expected_value < min_packet_threshold and observed_value < min_packet_threshold:
			e=0
		else:
			chi_sq_normal=chi_sq_normal+val_to_add

	for i in normal_only_list:
		observed_value= 0
		expected_value= (float(packets_seen)*curr_dict[i])
		if expected_value > 0:
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			# print(i,observed_value,expected_value,curr_dict[i],val_to_add)
			
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
	

	if type_of_attack=="normal_test":
		normal_chi_sq_list.append(chi_sq_normal)
		threshold_list_normal.append(scipy.stats.chi2.ppf(0.90,union_val))
	else:
		lf_chi_sq_list.append(chi_sq_normal)
		threshold_list_lf.append(scipy.stats.chi2.ppf(0.90,union_val))


	if union_val>0:
		print("################" + type_of_attack + "################ ")
		print("Window Number is: ",iteration_number)
		print("Chi-Square Value is ",chi_sq_normal)
		print("Total Number of Eq Classes seen are", union_val)
		print("Total Number of Packets Seen are", packets_seen)


	print("#############################")
	print("#############################")
	print("#############################")

	return 0

prev_list=[]
while True:
	time.sleep(5)
	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	p1.wait()

	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	p2.wait()

	bl_code=open("out1.txt","r")
	lines = bl_code.readlines()
	bl_code_line= lines[3]
	bl_code_array= bl_code_line[32:-1]
	bl_code_array= bl_code_array.split(", ")
	bl_code_reg=[]
	for val in bl_code_array:
		bl_code_reg.append(val)
	
	bl_code.close()

	bl_freq=open("out2.txt","r")
	lines = bl_freq.readlines()
	bl_freq_line= lines[3]
	bl_freq_array= bl_freq_line[29:-1]
	bl_freq_array= bl_freq_array.split(", ")
	bl_freq_reg=[]
	for val in bl_freq_array:
		bl_freq_reg.append(val)
	
	bl_freq.close()

	bl_code_reg= [int(i) for i in bl_code_reg]
	bl_freq_reg= [int(i) for i in bl_freq_reg]
	bl_pair_reg= tuple(zip(bl_code_reg,bl_freq_reg))

	# call function
	status1=chi_square_test(iteration_number,probab_normal,bl_pair_reg,prev_list,"normal_test")
	status2=chi_square_test(iteration_number,probab_link_failure,bl_pair_reg,prev_list,"link_failure_test")


	if status1== -1 or status2 == -1:
		normal_chi_sq_list= [math.log(x,2) for x in normal_chi_sq_list]
		lf_chi_sq_list= [math.log(x,2) for x in lf_chi_sq_list]
		threshold_list_normal=[math.log(x,2) for x in threshold_list_normal]
		threshold_list_lf= [math.log(x,2) for x in threshold_list_lf]
		normal_chi_sq_list=normal_chi_sq_list[2:len(normal_chi_sq_list)-3]
		lf_chi_sq_list= lf_chi_sq_list[2:len(lf_chi_sq_list)-3]
		threshold_list_lf= threshold_list_lf[2:len(threshold_list_lf)-3]
		threshold_list_normal= threshold_list_normal[2:len(threshold_list_normal)-3]
		x= range(1, len(normal_chi_sq_list) + 1)
		y1= normal_chi_sq_list
		y2= lf_chi_sq_list
		y3= threshold_list_normal
		y4= threshold_list_lf
		xlabel= 'window number'
		ylabel= 'log(chi sq deviation)'
		title_name= 'chi-sq devaition plot'
		plt.plot(x, y1, 'r',color='green',marker='o')
		plt.plot(x,y2,'r',color='red',marker='o')
		plt.plot(x,y3,'r',color='green',ls='--')
		plt.plot(x,y4,'r',color='red',ls='--')
		# attack_time= open("attack-time.txt",'r')
		# lines= attack_time.readlines()
		# line_to_read= lines[0]
		# atck_start_time= float(line_to_read[0])
		# atck_end_time = float(line_to_read[1])
		# plt.axvline(x=7,color='blue')
		# plt.axvline(x=12,color='blue')
		plt.savefig(save_image_to + str(title_name + '.png'))
		break

	prev_list= bl_pair_reg
	iteration_number= iteration_number + 1



for pid in pid_list:
    pid.wait()

