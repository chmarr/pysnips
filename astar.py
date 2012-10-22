#! /usr/bin/env python

import optparse, copy
import logging

logging.basicConfig ( level=logging.INFO )

cli_usage = "%prog: [options] ... argument"

cli_description = """\
Description of utility here
"""

cli_defaults = dict (
	example_num = 0,
	epsilon = 1.0,
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
		# 0=move piece up, 1=move piece right, 2=move piece down, 3=move piece left
		if self.blank_pos < self.xdim * (self.ydim-1): yield (0,1)
		if ( self.blank_pos % self.xdim ) != 0: yield (1,1)
		if self.blank_pos >= self.xdim: yield (2,1)
		if ( (self.blank_pos+1) % self.xdim ) != 0: yield (3,1)
		
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
	class PuzzleBoard ( GenericPuzzleBoard ):
		epsilon = new_epsilon
		xdim = x_dimension
		ydim = y_dimension
		goal_board = tuple ( range(1,xdim*ydim) + [None] )
		operations_blank_swaps_with = [ xdim, -1, -xdim, 1 ]
	return PuzzleBoard
		

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
	leaf_nodes = { initial_game_state: AStarNode(initial_game_state,0,initial_game_state.estimate_cost_to_goal()) }
	other_nodes = {}
	iterations = 0
	leaf_nodes_matched = 0
	other_nodes_matched = 0
	
	while True:
		logging.debug ( "%d leaf nodes %d other nodes", len(leaf_nodes), len(other_nodes) )
		if not leaf_nodes:
			raise ValueError ( "our list of nodes is empty! what?" )
		best_node = None
		best_estimate = None
		for node in leaf_nodes.values():
			if best_node is None or node.cost + node.estimate_to_goal < best_estimate:
				best_node = node
				best_estimate = node.cost + node.estimate_to_goal
		if iterations%1000 == 0:
			logging.info ( "leaf nodes %d other nodes %d best estimate %r leaf nodes matched %d other nodes matched %d", len(leaf_nodes), len(other_nodes), best_estimate, leaf_nodes_matched, other_nodes_matched )
		del leaf_nodes[best_node.game_state]
		other_nodes[best_node.game_state] = best_node
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
				found_node = leaf_nodes[new_state]
				leaf_nodes_matched += 1
				if new_cost < found_node.cost:
					logging.debug ( "new state is better than a leaf_node. replacing" )
				else:
					logging.debug ( "new state matches a leaf node at cost %r. discarding", found_node.cost )
					continue
			except KeyError:
				pass
				
			try:
				found_node = other_nodes[new_state]
				other_nodes_matched += 1
				if new_cost < found_node.cost:
					logging.debug ( "new state is better than an other node. replacing" )
				else:
					logging.debug ( "new state matches an other node at cost %r. discarding", found_node.cost )
					continue
			except KeyError:
				pass
				
			logging.debug ( "adding to node list" )
			a = AStarNode ( new_state, new_cost, estimate )
			a.operations_to_date = best_node.operations_to_date + [ ( operation, cost ) ]
			leaf_nodes[new_state] = a
		iterations += 1
				
				
examples = [
	[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None ],
	[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, None, 13, 14, 15, 12 ],
	[ 1, 3, 11, 8, 5, 4, 15, 10, 7, 2, 12, 13, 14, 9, 6, None ],
	[ 1, None, 3, 4, 6, 2, 11, 10, 5, 8, 7, 9, 14, 12, 15, 13 ],
	]
				
		
def sliding_puzzle ( example_num, epsilon ):

	PuzzleBoard = make_puzzleboard ( 4, 4, epsilon )

	board = PuzzleBoard ( board = examples[example_num] )
	
	end_state, cost, operations = a_star ( board )
	
	print end_state.board, cost, operations
	
	


def get_options ():
	parser = optparse.OptionParser ( usage=cli_usage, description=cli_description )
	parser.set_defaults ( **cli_defaults )
	
	parser.add_option ( "-n", "--example_num", type="int", help="Change the value [%default]" )
	parser.add_option ( "-e", "--epsilon", type="float" )
	opts, args = parser.parse_args ()
	
	# No arguments allowed
	if len(args) != 0:
		raise parser.error ( "no arguments expected" )

	return opts

if __name__ == "__main__":
	opts = get_options ()
	sliding_puzzle ( opts.example_num, opts.epsilon )
