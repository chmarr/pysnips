#! /usr/bin/env python

import optparse

cli_usage = "%prog: [options] ... argument"

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
# 		raise parser.error ( "no more than 3 arguments expected" )

	# All arguments are filenames
# 	opts.files = args

	return opts

if __name__ == "__main__":
	opts = get_options ()
	# main ( opts.files )