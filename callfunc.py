"""
	Call a function with the attributes of an object.
	
	Unlike using fn(**dict1), this will not raise an exception
	if the destination function does not have a particular parameter.
	Ie, the logic is "give the function the parameter if the function was expecting it."
	
	This is especially useful if you are collecting CLI arguments and passing them
	to one or more functions, as it saves having to "pick and choose" each of the
	arguments required. If you fill the Option object correctly, and there
	is a exact-name-match between the Values object and the to-be-called function,
	you can simply your code down to this:
	
	parser = optparse.OptionParser ()
	# ... add options and defaults as required
	opts, args = parser.parse_args ()
	opts.files = args  # An example. If arguments have other purposes, code accordingly
	
	call_fn_with_opts ( main, opts )
	
	If your program requires passing CLI options to two or more functions
	'call_fn_with_opts' will only pass the parameters it needs, and has the option
	to rename, include or exclude certain parameters, and pass additional parameters
	that might not have been included in the Values object.
	
	class Config ():
	# ...
	
	config = call_fn_with_opts ( Config, opts, exclude=['libpath'] )
	call_fn_with_opts ( main, opts, map={'cd':'homedir'}, config=config )
	
"""


def call_fn_with_opts ( main_function, opts, include=None, exclude=[], map={}, **kwargs ):
	co = main_function.func_code
	vars = co.co_varnames[:co.co_argcount]
	args = {}
	for v in vars:
		try:
			src = map[v]
			args[v] = getattr ( opts, src )
		except KeyError:
			if ( not include or v in include ) and v not in exclude:
				try:
					args[v] = getattr ( opts, v )
				except AttributeError:
					pass
	args.update ( kwargs )
	return main_function ( **args )
