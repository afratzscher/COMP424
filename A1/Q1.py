import numpy as np
import collections
import math

class state:
	def __init__(self,cost,depth,parent,positions,move,direction):
		self.depth = depth
		self.cost = cost
		self.parent = parent
		self.positions = positions
		self.move = move
		self.direction=direction

def get_index(positions):
	row,col = [*np.where(positions == 0)]
	return row[0], col[0]

def check_visited(direction, curr_state, positions, visited, val):
	for i in visited:
		if (positions == i).all():
			return None
	return state(curr_state.cost+1, curr_state.depth+1, curr_state, positions, val, direction)
	
def move(curr_state, direction, visited):
	positions = curr_state.positions.copy()
	row, col = get_index(positions)
	if direction is 'L':
		try: 
			positions[row, col], positions[row, col+1] = positions[row, col+1], positions[row, col]
			return check_visited(direction, curr_state, positions, visited, positions[row,col])
		except:
			return None
	if direction is 'R':
		try: 
			if col-1 >= 0: # accounts for list[-1] allowance
				positions[row, col], positions[row, col-1] = positions[row, col-1], positions[row, col]
				return check_visited(direction,curr_state, positions, visited, positions[row,col])
			else:
				return None
		except:
			return None
	if direction is 'U':
		try: 
			positions[row, col], positions[row+1, col] = positions[row+1, col], positions[row, col]
			return check_visited(direction, curr_state, positions, visited, positions[row,col])
		except:
			return None
	if direction is 'D':
		try: 
			if row-1 >= 0: # accounts for list[-1] allowance
				positions[row, col], positions[row-1, col] = positions[row-1, col], positions[row, col]
				return check_visited(direction, curr_state, positions, visited, positions[row,col])
			else:
				return None
		except:
			return None

def backtrack(goal_state, start_state):
	solution = []
	curr_state = goal_state 
	while not ((curr_state.positions == start_state.positions).all()):
		solution.insert(0, curr_state.direction)
		# print(curr_state.positions)
		curr_state = curr_state.parent
	# print(start_state.positions)
	return solution


''' RUNS BREADTH-FIRST SEARCH'''
def bfs(start_state):
	queue = []
	visited = []
	queue.append(start_state)
	visited.append(start_state.positions)
	curr_state = start_state

	while not (curr_state.positions == goal_state).all():
		curr_state = queue.pop(0)
		print(curr_state.positions)
		if not (curr_state.positions == goal_state).all():
			print('->')
		toadd = {}
		for i in ['L', 'R', 'U', 'D']:
			temp = move(curr_state, i, visited)
			if temp:
				toadd[temp.move] = temp
		ordered_add = collections.OrderedDict(sorted(toadd.items()))
		for key in ordered_add:
			visited.append(ordered_add[key].positions)
			queue.append(ordered_add[key])
	
	return curr_state.cost, backtrack(curr_state, start_state)

'''RUNS UNIFORM COST SEARCH'''
def uniform(start_state):
	queue = {}
	visited = []
	queue[0] = [start_state]
	visited.append(start_state.positions)
	curr_state = start_state

	k = 0
	while not (curr_state.positions == goal_state).all():
		curr_state = queue[min(queue.keys())].pop(0)
		if (len(queue[min(queue.keys())]) == 0):
			queue.pop(min(queue.keys()))
			print(curr_state.positions)
		else:
			print(curr_state.positions)
		if not (curr_state.positions == goal_state).all():
			print('->')
		toadd = {}
		for i in ['L', 'R', 'U', 'D']:
			temp = move(curr_state, i, visited)
			if temp:
				toadd[temp.move] = temp
		ordered_add = collections.OrderedDict(sorted(toadd.items()))
		for key in ordered_add:
			visited.append(ordered_add[key].positions)
			try:
				currlist = queue[ordered_add[key].cost]
			except:
				currlist = []
			currlist.append(ordered_add[key])
			# currlist.sort(key=lambda x: x.move, reverse=False)
			queue[ordered_add[key].cost] = currlist
	
	return curr_state.cost, backtrack(curr_state, start_state)

''' RUNS DEPTH-FIRST SEARCH'''
def dfs(start_state, *args):
	max_depth = math.inf
	if args:
		max_depth = args[0]
	queue = []
	visited = []
	queue.append(start_state)
	visited.append(start_state.positions)
	curr_state = start_state
	to_print = []
	to_print.append(start_state)

	while (not (curr_state.positions == goal_state).all()):
		if curr_state not in to_print:
			to_print.append(curr_state)

		toadd = {}
		for i in ['L', 'R', 'U', 'D']:
			temp = move(curr_state, i, visited)
			if temp:
				toadd[temp.move] = temp
		try: 
			minstate = min(toadd.keys())
			curr_state = toadd[minstate]
			if curr_state.depth <= max_depth:
				queue.append(toadd[minstate])
				visited.append(toadd[minstate].positions)
		except:
			try:
				curr_state = queue.pop()
			except:
				for i in to_print:
					print(i.positions)
					print('->')
				return None, None

		if curr_state.depth > max_depth:
			try:
				curr_state = queue.pop()
			except:
				for i in to_print:
					print(i.positions)
					print('->')
				return None, None
	if max_depth<5:
		for i in to_print:
			print(i.positions)
			print('->')
		print(curr_state.positions)
	return curr_state.cost, backtrack(curr_state, start_state)

''' RUNS ITERATIVE-DEEPENING SEARCH COST SEARCH'''
def ids(start_state, max_depth):
	depth  = 0
	cost = None
	print_list = []
	while depth <= max_depth:
		while cost is None:
			if depth > max_depth:
				return None, None
			print('depth: ', depth)
			cost, solution = dfs(start_state, depth)
			if cost:
				return cost, solution
			depth+=1

def main():
	global goal_state
	goal_state = [[0,1,2],[5,4,3]]
	start_state = state(0, 0, None, np.array(([[1,4,2],[5,3,0]])), None, None)
	print('----BFS----')
	cost, solution = bfs(start_state)
	print('COST: ', cost, '\nSOLUTION: ', solution, '\n')

	print('----UNIFORM----')
	cost, solution = uniform(start_state)
	print('COST: ', cost, '\nSOLUTION: ', solution, '\n')

	print('----DFS----')
	cost, solution = dfs(start_state)
	print('COST: ', cost, '\nSOLUTION: ', solution, '\n')

	print('----IDS----')
	cost, solution = ids(start_state, 3)
	print('COST: ', cost, '\nSOLUTION: ', solution, '\n')

if __name__ == "__main__":
	main()