import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from tabulate import tabulate
from random import shuffle

def generatePoints(numCities):
	x = np.random.uniform(0.0, 1.0, numCities)
	y = np.random.uniform(0.0, 1.0, numCities)

	return list(zip(x,y))

def euclidean(a,b):
	return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def getDistances(nodes, numCities):
	distances = np.zeros((numCities, numCities))
	for i in range(0, len(nodes)):
		for j in range(0, len(nodes)):
			distances[i][j] = euclidean(nodes[i], nodes[j])
	return distances

def bruteForce(distances, numCities):
	# based on https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/
	# assume start at first vertex in list
	min_cost = np.inf # initially min = infinity
	next_perm = list(permutations(list(range(0, numCities))))
	for index, i in enumerate(next_perm):
		curr_cost = 0
		prev = 0
		for idx in i:
			curr_cost +=  distances[prev][idx]
			prev = idx
		curr_cost += distances[idx][i[0]]
		if curr_cost < min_cost:
			min_cost = curr_cost
	return min_cost

def randomTour(distances, numCities):
	vertices = list(range(1,numCities))
	shuffle(vertices) #shuffles list
	cost = 0
	prev = 0
	for idx in vertices:
		cost +=  distances[prev][idx]
		prev = idx
	cost += distances[idx][0]
	return cost, vertices

def greedy(distances, randcost, path, numCities):
	# based on https://en.wikipedia.org/wiki/2-opt#:~:text=In%20optimization%2C%202%2Dopt%20is,already%20been%20suggested%20by%20Flood
	# start with random tour path
	best_cost = randcost
	path.insert(0,0)
	best_path = path
	iters=0

	curr_cost = best_cost
	curr_path = path
	neigh = 0
		
	# get neighbour min
	# always start at and end at first vertex
	while True:
		for i in range(1, numCities):
			for j in range(i+1, numCities):
				neig_path = (path[0:i])
				neig_path.extend(path[i:j+1][::-1])
				if j != (numCities-1):
					neig_path.extend(path[j+1:])
				
				#calculate cost
				prev = 0
				neig_cost = 0
				for idx in neig_path:
					neig_cost +=  distances[prev][idx]
					prev = idx
				neig_cost += distances[idx][0]
				#if better, replace
				if neig_cost < curr_cost:
					curr_cost = neig_cost
					curr_path = neig_path	
		if curr_cost >= best_cost:
			# print(iters)
			return best_cost
		else:
			best_cost = curr_cost
			path = curr_path
			iters+=1
	return best_cost

def main():
	numCities = 7
	allCosts = []
	randCosts = []
	greedyCosts = []
	numRand = 0
	numGreedy = 0
	for i in range(0, 100): # runs 100 times
		nodes = generatePoints(numCities)
		distances = getDistances(nodes, numCities)
		cost = bruteForce(distances, numCities)
		randcost, randpath = randomTour(distances, numCities)
		gcost = greedy(distances, randcost, randpath, numCities)
		if cost == randcost:
			numRand += 1
		if cost == gcost:
			numGreedy += 1
		allCosts.append(cost)
		randCosts.append(randcost)
		greedyCosts.append(gcost)

	print("******For {} cities******".format(numCities))
	print(tabulate([['Brute-force', np.min(allCosts), np.max(allCosts), np.mean(allCosts), np.std(allCosts)], 
		['Random', np.min(randCosts), np.max(randCosts), np.mean(randCosts), np.std(randCosts), numRand],
		['Greedy', np.min(greedyCosts), np.max(greedyCosts), np.mean(greedyCosts), np.std(greedyCosts), numGreedy]], 
		headers=['', 'Min', 'Max', 'Mean', 'Std', '#optimal'], tablefmt='orgtbl'))

	numCities = 100
	randCosts = []
	greedyCosts = []
	
	for i in range(0, 100): # runs 100 times
		nodes = generatePoints(numCities)
		distances = getDistances(nodes, numCities)
		randcost, randpath = randomTour(distances, numCities)
		gcost = greedy(distances, randcost, randpath, numCities)
		randCosts.append(randcost)
		greedyCosts.append(gcost)

	print("******For {} cities******".format(numCities))
	print(tabulate([['Random', np.min(randCosts), np.max(randCosts), np.mean(randCosts), np.std(randCosts)],
		['Greedy', np.min(greedyCosts), np.max(greedyCosts), np.mean(greedyCosts), np.std(greedyCosts)]], 
		headers=['', 'Min', 'Max', 'Mean', 'Std'], tablefmt='orgtbl'))
	
if __name__ == "__main__":
	main()
