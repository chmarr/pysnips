#! /usr/bin/env python

import optparse

# import logging
## Edit the formatting to your liking. What is shown is rather verbose.
## We assume WARNING is sufficient for any logging needed before options are parsed.
# logging.basicConfig ( level=logging.WARNING, format="%(asctime)s %(processName)s[%(process)d]: %(name)s: %(message)s" )
# logger = logging.getLogger( __name__ if __name__!="__main__" else "main" )

cli_usage = "%prog [options] ... arguments"

cli_description = """\
Description of utility here
"""

cli_defaults = dict (
	option1 = "default1",
)

def get_options ():
	parser = optparse.OptionParser ( usage=cli_usage, description=cli_description )
	parser.set_defaults ( **cli_defaults )
	
# 	parser.add_option ( "-x", "--ecks", action="store_true", help="Do the thing" )
	
# 	parser.add_option ( "-i", "--thing", type="int", help="Change the value [%default]" )
	
# 	parser.add_option ( "-n", "--name", type="str", help="Change the name [%default]" )

# 	def set_log_level ( option, opt, value, parser, log_level=None ):
# 		if log_level is None:
# 			try:
# 				log_level = int(value)
# 			except TypeError:
# 				log_level = value
# 		logging.get_logger().setLevel ( log_level )
# 	parser.add_option ( "--log-level", type="str", action="callback", callback=set_log_level )
# 	parser.add_option ( "-v", "--verbose", action="callback", callback=set_log_level, callback_kwargs={'log_level':logging.INFO} )
# 	parser.add_option ( "-d", "--debug", action="callback", callback=set_log_level, callback_kwargs={'log_level':logging.DEBUG} )

# 	def log_syslog ( option, opt, value, parser ):
# 		from pysnips import logging_basic_syslog
# 		logging_basic_syslog ( value )
#   parser.add_option ( "--syslog-facility", type="str", action="callback", callback=log_syslog )
	
	opts, args = parser.parse_args ()
	
	# No arguments allowed
# 	if len(args) != 0:
# 		raise parser.error ( "no arguments expected" )

	# Fixed arguments
# 	if len(args) != 3:
# 		raise parser.error ( "exactly 3 arguments expected" )

	# Variable arguments
# 	if len(args) < 3:
# 		raise parser.error ( "at least 3 arguments expected" )
# 	if len(args) > 5:
# 		raise parser.error ( "no more than 5 arguments expected" )

	# All arguments are filenames
# 	opts.files = args

	# First argument is a thing, others are filenames
# 	opts.thing = args[0]
# 	opts.files = args[1:]

	return opts

if __name__ == "__main__":
	opts = get_options ()

	# Simple option parsing
# 	main ( opts.files )
	
	# If number/complexity of options is high, use pysnips.call_fn_with_opts
# 	from pysnips import call_fn_with_opts
# 	call_fn_with_opts ( main, opts )	
