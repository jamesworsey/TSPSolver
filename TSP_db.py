import random
import math
import time
import copy
import sys

import sqlite3

import matplotlib.pyplot as plt

#Connect to databasex
conn = sqlite3.connect('TSP_db.db')
c = conn.cursor()

###ADD problem to database
if(sys.argv[2] == 'ADD'):

	file_in = (sys.argv[3])
	try:
		infile = open(file_in, 'r')
	except IOError:
		print('File could not be opened.')
		exit()
	name = infile.readline().strip().split()[1] # NAME
	fileType = infile.readline().strip().split()[1] # TYPE
	comment = infile.readline().strip().split()[1] # COMMENT
	dimension = infile.readline().strip().split()[2] # DIMENSION
	edge_weight_type = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
	infile.readline()
	nodes = [None] * int(dimension)
	x = [None] * int(dimension)
	y = [None] * int(dimension)
	for i in range(0, int(dimension)):
	    nodes[i],x[i],y[i] = infile.readline().strip().split()[:]

	node_list = (', '.join(nodes))
	x_list = (', '.join(x))
	y_list = (', '.join(y))

	name = sys.argv[1]

	c.execute("INSERT INTO problems (Name,Dimension,Nodes,X,Y) VALUES (?, ?, ?, ?, ?)",(name,dimension,node_list,x_list,y_list))
	conn.commit()

###FETCH best know solution
if(sys.argv[2] == 'FETCH'):
	problem_name = (sys.argv[1])
	item = c.execute('SELECT * FROM solutions WHERE Problem_name = ?', (problem_name,))
	rows = c.fetchall()

	if not rows:
		print("Solution is not in database.")
		exit()

	min_distance = rows[0][1]
	optimal_solution_index = 0
	for i in range(len(rows)):
		if rows[i][1] < min_distance:
			min_distance = rows[i][1]
			optimal_solution_index = i

	optimal_route = (rows[optimal_solution_index][2].split(","))
	for i in range(len(optimal_route)):
		optimal_route[i] = int(optimal_route[i])
	print("")
	print(problem_name)
	print("Shortest found tour length: ", rows[optimal_solution_index][1])
	print("Tour:")
	for i in range(len(optimal_route)-1):
 		print((optimal_route[i] + 1))
	print(-1)


###LOAD problem from database SOLVE and STORE
if(sys.argv[2] == 'SOLVE'):
	#Parameters
	problem_name = (sys.argv[1])
	item = c.execute('SELECT * FROM problems WHERE Name = ?', (problem_name,))
	rows = c.fetchall()

	if not rows:
		print("Problem is not in database.")
		exit()
	for row in rows:
		name = row[0]
		dimension = row[1]
		nodes = [int(e) for e in row[2].split(",")]
		x = [float(e) for e in row[3].split(",")]
		y = [float(e) for e in row[4].split(",")]

	#MATPLOTLIB
	plt.plot(x, y)
	plt.show()
	##############

	cities = [] 
	total_cities = int(dimension)

	coordinates = [list(e) for e in zip(x,y)]
	for i in range(len(nodes)):
		cities.append([i,[coordinates[i][0],coordinates[i][1]]])
	#Append starting city to finish.
	cities.append(cities[0])

	timer = int(sys.argv[3])
	# Close input file

	###Generic functions
	#Calculate total distance between cities
	def calc_distance(cities):
		total_distance = 0
		for i in range(total_cities):
			total_distance += math.sqrt(((cities[i][1][0] - cities[i+1][1][0])**2)+((cities[i][1][1] - cities[i+1][1][1])**2))
		return(total_distance)

	#Swap elements i and j in an array
	def swap(element, i, j):
		temp = element[i]
		element[i] = element[j]
		element[j] = temp

	record_distance = float("inf")

	###Genetic 
	#Build population
	population = []
	total_pop = 2000
	fitness = [0] * total_pop

	for i in range(total_pop):
		population.append(cities[:])
		population[i][1:len(cities)-1] = random.sample(population[i][1:len(cities)-1],((len(cities)-1)-1))

	def calculate_fitness():
		global record_distance
		global best_route
		for i in range(total_pop):
			distance = calc_distance(population[i])
			if(distance < record_distance):
				record_distance = distance
				best_route = copy.deepcopy(population[i])
			fitness[i] = 1 / float(distance + 1)

	def normalize_fitness():
		sum = 0
		for fit in fitness:
			sum += fit
		for i in range(total_pop):
			fitness[i] = fitness[i] / sum


	def next_gen():
		new_population = [0] * total_pop

		j = 0
		for i in range(total_pop):
			if fitness[i] >= max(fitness) * 0.99:
				new_population[j] = population[i]
				j+=1
				if(j == 200):
					break

		for i in range(j,total_pop):
			orderA = selection(population, fitness)
			orderB = selection(population, fitness)
			order = breed(orderA,orderB)
			order = mutate(order)

			new_population[i] = order

		return new_population

	def selection(population_list, prob):
		r = random.random()
		index = 0
		while (r > 0):
			r = r - prob[index]
			index += 1
		index -= 1
		return population_list[index]

	crossover_rate = 1.00

	def breed(orderA,orderB):
		new_order = []
		if(random.random() < crossover_rate):
			start = random.randint(1,len(orderA)-1)
			end = random.randint(start,len(orderA)-1)

			orderA = orderA[start:end]

			for i in range(len(orderB)):
				if orderB[i] not in orderA:
					new_order.append(orderB[i])
			j = 0
			for i in range(start,start+len(orderA)):
				new_order.insert(i,orderA[j])
				j += 1
		else:
			new_order = orderA
		return(new_order)


	mutation_rate = 0.025
	def mutate(order):
		if(random.random() < mutation_rate):
			indexA= random.randint(1,len(order)-2) #dont pick 1st or last
			indexB = random.randint(1,len(order)-2)
			swap(order,indexA,indexB)
		return(order)



	#Loop
	t_end = time.time() + timer #Run for timer seconds
	while(time.time() < t_end):
		print('\r', "Time left: ", t_end - time.time(), end="")
		calculate_fitness()
		normalize_fitness()
		population = next_gen()

	print("")
	print(name)
	#print("Shortest found tour length: ", record_distance)
	#print("Tour:")
	#for i in range(len(best_route)-1):
 	#	print(best_route[i][0] + 1)
	#print(-1)

	x = []
	y = []
	for i in range(len(best_route)):
		x.append(best_route[i][1][0])
		y.append(best_route[i][1][1])

	print(x)
	print(y)

	
	plt.plot(x, y)
	plt.show()

	for i in range(len(best_route)):
		best_route[i] = best_route[i][0]

	best_route = str(best_route).strip('[]')
	c.execute("INSERT INTO solutions (Distance,Node_order, Problem_name) VALUES (?, ?, ?)",(record_distance,best_route,name))
	conn.commit()




















