#! /usr/bin/env python

import optparse, copy, heapq
import logging

logging.basicConfig ( level=logging.INFO )

cli_usage = "%prog: [options]"

cli_description = """\
Demonstrate A* search using sliding puzzle.
"""

cli_defaults = dict (
	example_num = 0,
	epsilon = 1,
)


class GenericPuzzleBoard ( object ):

	epsilon = 1

	def __init__ ( self, board=None ):
		if board is None:
			self.board = self.goal_board
		else:
			self.board = tuple(board)
		self.blank_pos = self.board.index ( None )
		
	def default_board ( self ):
		return range(1,self.xdim*self.ydim) + [None]
		
	def set_board ( self, board ):
		if isinstance ( board, PuzzleBoard ):
			self.board = list(board.board)
		else:
			self.board = list(board)
			
	def is_goal ( self ):
		return self.board == self.goal_board
		
	def valid_operations_and_costs ( self ):
		if self.blank_pos < self.xdim * (self.ydim-1): yield ('u',1)
		if ( self.blank_pos % self.xdim ) != 0: yield ('r',1)
		if self.blank_pos >= self.xdim: yield ('d',1)
		if ( (self.blank_pos+1) % self.xdim ) != 0: yield ('l',1)
		
	def copy_board ( self, operation=None ):
		if operation is not None:
			temp_board = list(self.board)
			new_pos = self.blank_pos+self.operations_blank_swaps_with[operation]
			temp_board[self.blank_pos] = temp_board[new_pos]
			temp_board[new_pos] = None
		else:
			temp_board = self.board
		b = self.__class__ ( temp_board )
		return b
		
	def estimate_cost_to_goal ( self ):
		def distance ( x, y ):
			xd, xm = divmod(x,self.xdim)
			yd, ym = divmod(y,self.xdim)
			return abs(xd-yd) + abs(xm-ym)
		total = 0
		for index, val in enumerate(self.board):
			if val == None: continue
			total += distance ( index, val-1 )
		return total * self.epsilon
			
	def __eq__ ( self, other ):
		return self.board == other.board
		
	def __repr__ ( self ):
		return "PuzzleBoard ( %r, %r, %r )" % ( self.xdim, self.ydim, self.board )
		
	def __hash__ ( self ):
		return hash(self.board)
		

def make_puzzleboard ( x_dimension, y_dimension, new_epsilon=1 ):
	"""Make a puzzleboard class with specific X and Y dimensions, and epsilon"""
	class PuzzleBoard ( GenericPuzzleBoard ):
		epsilon = new_epsilon
		xdim = x_dimension
		ydim = y_dimension
		goal_board = tuple ( range(1,xdim*ydim) + [None] )
		operations_blank_swaps_with = dict ( u=xdim, r=-1, d=-xdim, l=1 )
	return PuzzleBoard


# Game states must be objects with the following methods
#
# is_goal () - returns True if the current state is a goal
# valid_operations_and_costs () - returns a list of tuples of form ( op, cost )
#              where "op" represents an operation (may be any type), and
#              "cost" is the cost of that operation (may be any scalar type).
#              A generator is allowed.
# copy_board ( operation=None ) - creates a new state from the current
#              if "operation" is not None, then apply that operation to the state
# estimate_cost_to_goal () - returns a "permissive" estimate of the cost
#              from this state to the goal state. Estimate <= Actual
# __eq__ ( other ) - returns True if the game states are equal
# __hash__ () - returns a hash suitable for the game state.
#               If game states are equal, the hash must also be equal
#
# To prune duplicated states, states must be both comparable, and be
# used as a key to a dictionary, thus the __eq__ and __hash__ methods.
#
# a_star will maintain a list of operations preceeding each state, but
# the game state is allowed to keep track of this too, and even use
# it in the determination of equal game states. However, unless that
# is important for costs, do not do this as it will significantly
# slow down the a_star search.
#
# "operations" may be any type. a_star will feed the "copy_board" method
# operations it receives from the "valid_operations_and_costs" method
#
# costs and estimates may be any type that can be compared and added
		
class AStarNode ( object ):
	def __init__ ( self, game_state, cost, estimate_to_goal=None ):
		self.game_state = game_state
		self.cost = cost 
		self.estimate_to_goal = estimate_to_goal
		self.operations_to_date = []
	def __eq__ ( self, other ):
		return self.game_state == other.game_state
	def __hash__ ( self ):
		return hash(self.game_state)

def a_star ( initial_game_state ):

	a = AStarNode(initial_game_state,0,initial_game_state.estimate_cost_to_goal())
	nodes = { initial_game_state:a }
	queue = []
	heapq.heappush ( queue, (a.cost+a.estimate_to_goal,a) )

	iterations = 0
	nodes_matched = 0
	nodes_replaced = 0
	
	while True:
		logging.debug ( "%d nodes %d queued", len(nodes), len(queue) )
		if not queue:
			raise ValueError ( "our queue is empty! what?" )
		best_estimate, best_node = heapq.heappop ( queue )
		if iterations%1000 == 0:
			logging.info ( "nodes %d queue %d best estimate %r nodes matched %d nodes_replaced %d", len(nodes), len(queue), best_estimate, nodes_matched, nodes_replaced )
		logging.debug ( "best potential is %r with cost %r and estimate %r", best_node.game_state, best_node.cost, best_node.estimate_to_goal )
		if best_node.game_state.is_goal ():
			logging.debug ( "optimal goal found. end state %r cost %r operations %r", best_node.game_state, best_node.cost, best_node.operations_to_date )
			return best_node.game_state, best_node.cost, best_node.operations_to_date
		for operation, cost in best_node.game_state.valid_operations_and_costs ():
			new_state = best_node.game_state.copy_board ( operation )
			new_cost = best_node.cost + cost
			estimate = new_state.estimate_cost_to_goal()
			logging.debug ( "operation %r cost %r creates new state %r with estimate %r", operation, cost, new_state, estimate )
			
			try:
				found_node = nodes[new_state]
				nodes_matched += 1
				if new_cost < found_node.cost:
					logging.debug ( "new state is better than a matched node. replacing and adding back into queue" )
					nodes_replaced += 1
				else:
					logging.debug ( "new state matches a node with cost %r. discarding", found_node.cost )
					continue
			except KeyError:
				pass
				
			a = AStarNode ( new_state, new_cost, estimate )
			a.operations_to_date = best_node.operations_to_date + [ ( operation, cost ) ]

			logging.debug ( "adding to node list" )
			nodes[new_state] = a			
			heap_key = ( new_cost+estimate, a )
			heapq.heappush ( queue, heap_key )
		iterations += 1
				
				
examples = [
	[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None ],
	[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, None, 13, 14, 15, 12 ],
	[ 1, 3, 11, 8, 5, 4, 15, 10, 7, 2, 12, 13, 14, 9, 6, None ],
	[ 1, None, 3, 4, 6, 2, 11, 10, 5, 8, 7, 9, 14, 12, 15, 13 ],
	[ None, 12, 9, 13, 15, 11, 10, 14, 3, 7, 2, 5, 4, 8, 6, 1 ], # needs 80 moves - highest possible
	]
				
		
def sliding_puzzle ( example_num, epsilon ):

	PuzzleBoard = make_puzzleboard ( 4, 4, epsilon )

	board = PuzzleBoard ( board = examples[example_num] )
	
	end_state, cost, operations = a_star ( board )
	
	print end_state.board, cost, operations
	
	


def get_options ():
	parser = optparse.OptionParser ( usage=cli_usage, description=cli_description )
	parser.set_defaults ( **cli_defaults )
	
	parser.add_option ( "-n", "--example_num", type="int", help="example puzzle number [%default]" )
	parser.add_option ( "-e", "--epsilon", type="float" )
	opts, args = parser.parse_args ()
	
	# No arguments allowed
	if len(args) != 0:
		raise parser.error ( "no arguments expected" )

	return opts

if __name__ == "__main__":
	opts = get_options ()
	sliding_puzzle ( opts.example_num, opts.epsilon )
