# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)

#Aleksas Murauskas 
#260718389
#ECSE 422
#Programming Assignemnt

import edge_generator
import sys
import edge
from possibleSystem import possibleSystem

def main():
	file_path ="input.txt"
	print("Please set input file path:", end=" ")
	file_path = input()
	reliability_goal= .4
	cost_constraint=100
	reliability_goal = input("Please enter reliability goal: ")
	cost_constraint = input("Please enter cost constraint: ")

	city_list, edge_list = edge_generator.generate(file_path)

	print("System Variables:")
	print(city_list)
	print(edge_list)
	print("Reliability Goal:",reliability_goal)
	print("Cost Constraint:",cost_constraint)

	print("Part A: Meet a Reliability goal")
	mst_tree, mst_reliability, mst_cost, remaining_edges=prim_Algo_R(city_list, edge_list, 1)
	

	if(mst_reliability >= float(reliability_goal)): 
		print("The Mininmum Spanning Tree meets the goal")
		print("Reliability: ", mst_reliability)
		print("Cost: ", mst_cost)
		print(mst_tree)
	else:
		print("MST Does not meet goal")
		systems = AugmentMST(float(reliability_goal), mst_tree, mst_reliability, mst_cost, remaining_edges, city_list)
		best = find_best_soution(systems,1,edge_list,cost_constraint,reliability_goal)
		print("The Following System meets the goal")
		print("Reliability: ", best.reliability)
		print("Cost: ", best.cost)
		print(best.edge_list)

	print("Part B: Maximize Reliability Subject to a Cost Constraint")
	systems=AugmentMST(float(reliability_goal), mst_tree, mst_reliability, mst_cost, remaining_edges, city_list)
	optimized = find_best_soution(systems,1,edge_list,cost_constraint,reliability_goal)
	if(optimized.reliability==0):
		print("Could not achieve desired network given constraints")
	else:
		print("Best Result given constraints:")
		print("The Following System meets the goal")
		print("Reliability: ", optimized.reliability)
		print("Cost: ", optimized.cost)
		print(optimized.edge_list)

def prim_Algo_R(city_list, edge_list, type): #Create a network on reliability 
	nodes_needed= len(city_list)
	#Declare the lists to start the program with 
	mst=list()
	tot_list=edge_list.copy()
	remain_list = tot_list.copy()
	nodes_attached = [0]* nodes_needed #0 or 1 to determine a vertice has been added to MST
	mst_cost=0
	mst_rely=0

	#sort the list
	#The tot list of edges is sorted
	if(type ==1):
		tot_list.sort(key=lambda r: r.reliability, reverse=True)
	else:
		tot_list.sort(key=lambda c: c.cost, reverse=False)
	#Create the initial tree
	best_edge =tot_list[0]
	#Add edge to MST 
	mst.append(best_edge)
	mst_rely= best_edge.reliability
	mst_cost=best_edge.cost
	#Update Vertice list
	nodes_attached[convert_letter_to_index(best_edge.vertice_1)] = 1
	nodes_attached[convert_letter_to_index(best_edge.vertice_2)] = 1
	remain_list.remove(best_edge)
	
	ind=1
	while(len(mst)!=nodes_needed-1):
		#Work through the next edge left
		new_edge = tot_list[ind]

		v1=convert_letter_to_index(new_edge.vertice_1)
		v2=convert_letter_to_index(new_edge.vertice_2)
		if(nodes_attached[v1]==0 or nodes_attached[v2]==0):
			mst.append(new_edge)
			remain_list.remove(new_edge)
			nodes_attached[v1]=1
			nodes_attached[v2]=1
			mst_cost+=new_edge.cost
			mst_rely=mst_rely*new_edge.reliability
		ind+=1
	return mst, mst_rely, mst_cost, remain_list


def AugmentMST(goal, mst_tree, mst_reliability, mst_cost, remaining_edges, city_list):
	edges = mst_tree.copy()
	mst = mst_tree.copy()
	last_addition=-1
	networks= []
	mst_network =possibleSystem(edges,mst_cost,mst_reliability)
	networks.append(mst_network)
	augments =remaining_edges.copy()
	active= edges.copy()
	temp=[]
	#work throught the edges
	while(len(augments)>0):
		temp =[]
		for x in range(len(augments)):
			new_edge= augments[x]
			active = active.copy()
			active.append(new_edge)
			#Find the cost and reliabilty of augmented system
			edge_list,tot_cost, tot_rel=getSystemReliability(active, city_list)
			#print(edge_list)
			new_network= possibleSystem(tot_cost, tot_rel,edge_list)
			networks.append(new_network)
			temp.append(new_network)
		best_of_temp=temp[0]
		for elem in temp:
			if((elem.cost <best_of_temp.cost) and (elem.reliability>best_of_temp.reliability)):
				best_of_temp = elem
		edges.append(best_of_temp.edge_list[last_addition])
		augments.remove(best_of_temp.edge_list[last_addition])
	return networks

#Will determine the system reliability and cost, return a possible system 
def getSystemReliability(edge_list, node_list):
	tot_cost=0
	tot_rel=0
	num_edges=len(edge_list)
	num_nodes=len(node_list)
	
	#Compute cost of system
	for e in edge_list:
		tot_cost+=e.cost
	
	#Compute Reliability of System
	for x in range(2**num_edges):
		temp = list()
		nodes_attached= [0]*num_nodes
		edge_rel= [-1]*num_edges
		tracker = list('{0:0b}'.format(x))
		tracker = tracker[::-1]
		for y in range(num_edges):
			if(y<len(tracker)):
				if(tracker[y]=='1'):
					ed=edge_list[y]
					n1 =convert_letter_to_index(ed.vertice_1)
					n2 = convert_letter_to_index(ed.vertice_2)
					temp.append(ed)
					nodes_attached[n1]=1
					nodes_attached[n2]=1
					edge_rel[y]=ed.reliability
				else:
					edge_rel[y]=1-edge_list[y].reliability
			else:
				edge_rel[y]=1-edge_list[y].reliability
		if(num_nodes==sum(nodes_attached)):
			sub_rely=1
			for z in range(len(edge_rel)):
				sub_rely*=edge_rel[z]
			tot_rel+=sub_rely
	return edge_list,tot_cost, tot_rel

def convert_letter_to_index(vertice_name):
	return  ord(vertice_name) - 65 

def find_best_soution(systems, solution_type, edge_list, cost, goal):
	best = possibleSystem(100000, 2, edge_list)
	if(solution_type==1): #Answer Part A
		systems.sort(key=lambda a: a.reliability, reverse=False)
		for system in systems:
			if(system.r>=best.r):
				if(system.r>=goal):
					best=system
	else: #Answer Part B
		systems.sort(key=lambda a: a.cost, reverse=True)
		best =possibleSystem(1,0, edge_list)
		for system in systems:
			if(system.c<=cost):
				if(system.r>=best.r):
					if(system.r>=goal):
						best=system
	return best


main()


