# # #!/bin/bash
# #This is a comment

# # my_dir= $(pwd)



# p4dir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/p4
# cpdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/control_plane
# kvdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/kv_store
# memdir=/home/p4/netcache-check-point-thesis-before-bash/netcache-master/src/kv_store/data
# PID= echo "$$"

# gnome-terminal -- bash -c "cd $p4dir; sudo p4run --config p4app_8_1.json;"&
# PID1=$!

# sleep 10

# gnome-terminal -- bash -c "cd $cpdir; sudo python controller.py;"&
# PID2=$!

# sleep 3

# gnome-terminal -- bash -c "cd $p4dir; ./init_servers.sh 8;bash"&
# PID3=$! && echo SUCCESS || echo FAIL


# sleep 3
# gnome-terminal -- bash -c "cd $kvdir; mkdir -p results; mx client1 python3 exec_queries.py --n-servers 8 --suppress --input data/traffic.txt;"&
# PID4=$! && echo SUCCESS || echo FAIL


# sleep 3 
# gnome-terminal -- bash -c "cd $p4dir; python observed.py; bash;"&
# PID5=$! && echo SUCCESS || echo FAIL


# sleep 300

# for i in ` ps -ef | grep -e 'bash' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	# if [[ $i -ne $PID ]]
# 	# then
# 	# 	kill $i
# 	# fi
# 	sudo kill $i
# done


# for i in ` ps -ef | grep -e 'python' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	if [[ $i -ne $PID ]]
# 	then
# 		kill $i
# 	fi
# 	# sudo kill $i
# done

# for i in ` ps -ef | grep -e 'p4run' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	if [[ $i -ne $PID ]]
# 	then
# 		kill $i
# 	fi
# 	# sudo kill $i
# done


# for i in ` ps -ef | grep -e 'mx' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	if [[ $i -ne $PID ]]
# 	then
# 		kill $i
# 	fi
# 	# sudo kill $i
# done

# for i in ` ps -ef | grep -e 'netcache' | grep -v 'grep' | awk '{print $2}'`
# do 	
# 	if [[ $i -ne $PID ]]
# 	then
# 		kill $i
# 	fi
# 	# sudo kill $i
# done



























# #!/bin/bash
#This is a comment

# my_dir= $(pwd)



currdir="/home/p4/Blink"
PID= echo "$$"


for((j=0;j<=0;j++));
do

	gnome-terminal -- bash -c "cd $currdir; sudo p4run;"&
	PID1=$!

	sleep 15

	gnome-terminal -- bash -c "cd $currdir; sudo python -m controller.blink_controller --port 10000 --log_dir log --log_level 20 --routing_file topologies/5switches_routing.json --threshold 15 --topo_db topology.db;"&
	PID2=$!

	sleep 3

	gnome-terminal -- bash -c "cd $currdir; python -m controller.run_p4_controllers --topo_db topology.db --controller_ip localhost --controller_port 10000 --routing_file topologies/5switches_routing.json;"&
	PID3=$!

	sleep 3

	gnome-terminal -- bash -c "cd $currdir; mx h2; python -m traffic_generation.run_servers --ports 11000,11040 --log_dir log_traffic;"&
	PID4=$!

	sleep 3

	gnome-terminal -- bash -c "cd $currdir; mx h1; python -m traffic_generation.run_clients --dst_ip 10.0.5.2 --src_ports 11000,11040 --dst_ports 11000,11040 --ipd 1 --duration 100 --log_dir log_traffic/;"&
	PID5=$!
	sleep 1

	gnome-terminal --bash -c "cd $currdir; speedometer -t s1-eth2;"


	# gnome-terminal -- bash -c "cd $currdir; python observed.py;"&
	# PID6=$!

	sleep 40

	
	# gnome-terminal -- bash -c "cd $p4dir; python observed.py; bash;"&
	# PID6=$!

	


	for i in ` ps -ef | grep -e 'p4run' | grep -v 'grep' | awk '{print $2}'`
	do 	
		echo $j
		# if [[ $i -ne $PID ]]
		# then
		# 	kill $i
		# fi
		sudo kill $i
	done

	for i in ` ps -ef | grep -e 'python' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'python3' | grep -v 'grep' | awk '{print $2}'`
	do 	
		# if [[ $i -ne $PID ]]
		# then
		# 	kill $i
		# fi
		sudo kill $i
	done

	for i in ` ps -ef | grep -e 'mx' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'kv_store' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done

	for i in ` ps -ef | grep -e 'netcache' | grep -v 'grep' | awk '{print $2}'`
	do 	
		if [[ $i -ne $PID ]]
		then
			kill $i
		fi
		# sudo kill $i
	done


	




done




