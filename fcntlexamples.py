
def make_nonblocking ( f, nonblocking=True ):
	"""Make fd 'f' (or a file-like object) blocking or non-blocking.
	This is not compatible with 'readline' or any function that expects
	to block to wait for a full message."""

	import os, fcntl
	
	flags = fcntl.fcntl ( f, fcntl.F_GETFL )
	if nonblocking:
		flags |= os.O_NONBLOCK
	else:
		flags &= ~os.O_NONBLOCK
	fcntl.fcntl( f, fcntl.F_SETFL, flags )
