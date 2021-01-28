import numpy as np
import collections

class state:
	def __init__(self,cost,depth,parent,positions,move):
		self.depth = depth
		self.cost = cost
		self.parent = parent
		self.positions = positions
		self.move = move

def get_index(positions):
	row,col = [*np.where(positions == 0)]
	return row[0], col[0]

def check_visited(direction, curr_state, positions, visited):
	for i in visited:
		if (positions == i).all():
			return None
	return state(curr_state.cost+1, curr_state.depth+1, curr_state, positions, direction)
	
def move(curr_state, direction, visited):
	positions = curr_state.positions.copy()
	row, col = get_index(positions)
	if direction is 'L':
		try: 
			positions[row, col], positions[row, col+1] = positions[row, col+1], positions[row, col]
			return check_visited(direction, curr_state, positions, visited), positions[row,col]
		except:
			return None, None
	if direction is 'R':
		try: 
			if col-1 >= 0: # accounts for list[-1] allowance
				positions[row, col], positions[row, col-1] = positions[row, col-1], positions[row, col]
				return check_visited(direction,curr_state, positions, visited), positions[row,col]
			else:
				return None, None
		except:
			return None, None
	if direction is 'U':
		try: 
			positions[row, col], positions[row+1, col] = positions[row+1, col], positions[row, col]
			return check_visited(direction, curr_state, positions, visited), positions[row,col]
		except:
			return None, None
	if direction is 'D':
		try: 
			if row-1 >= 0: # accounts for list[-1] allowance
				positions[row, col], positions[row-1, col] = positions[row-1, col], positions[row, col]
				return check_visited(direction, curr_state, positions, visited), positions[row,col]
			else:
				return None, None
		except:
			return None, None

def backtrack(goal_state, start_state):
	solution = []
	curr_state = goal_state 
	while not ((curr_state.positions == start_state.positions).all()):
		solution.insert(0,curr_state.move)
		print(curr_state.positions)
		curr_state = curr_state.parent
	print(start_state.positions)
	return solution


''' RUNS BREADTH-FIRST SEARCH'''
def bfs(start_state):
	print('starting BFS')
	queue = []
	visited = []
	queue.append(start_state)
	visited.append(start_state.positions)
	curr_state = start_state

	while not (curr_state.positions == goal_state).all():
		curr_state = queue.pop(0)
		toadd = {}
		for i in ['L', 'R', 'U', 'D']:
			temp, moved_val = move(curr_state, i, visited)
			if temp:
				toadd[moved_val] = temp
		ordered_add = collections.OrderedDict(sorted(toadd.items()))
		for key in ordered_add:
			visited.append(ordered_add[key].positions)
			queue.append(ordered_add[key])
	
	return curr_state.cost, backtrack(curr_state, start_state)

''' RUNS DEPTH-FIRST SEARCH'''
def dfs(start_state):
	print('starting DFS')
	queue = []
	visited = []
	visited.append(start_state.positions)
	curr_state = start_state

	k = 0
	while not (curr_state.positions == goal_state).all():
		k+=1
		toadd = {}
		for i in ['L', 'R', 'U', 'D']:
			temp, moved_val = move(curr_state, i, visited)
			if temp:
				toadd[moved_val] = temp
		try: 
			minstate = min(toadd.keys())
			curr_state = toadd[minstate]
			queue.append(toadd[minstate])
			visited.append(toadd[minstate].positions)
		except:
			curr_state = queue.pop()
	
	
	return curr_state.cost, backtrack(curr_state, start_state)

def main():
	global goal_state
	goal_state = [[0,1,2],[5,4,3]]
	start_state = state(0, 1, None, np.array(([[1,4,2],[5,3,0]])), None)
	cost, solution = dfs(start_state)
	print('COST: ', cost, '\nSOLUTION: ', solution)

if __name__ == "__main__":
	main()