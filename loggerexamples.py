import logging, os
from logging.handlers import SysLogHandler

def logging_basic_syslog ( facility="user", level=None ):

	"Set up a basic logging configuration using the local syslog."

	if os.path.exists ( "/dev/log" ):
		path = "/dev/log"
	elif os.path.exists ( "/var/run/syslog" ):
		path = "/var/run/syslog"
	else:
		path = ( 'localhost', SysLogHandler.SYSLOG_UDP_PORT )

	syslog_handler = SysLogHandler ( path )
	# TODO: on OS/X processName ends up as "MainProcess" rather than argv[0]
	formatter = logging.Formatter ( "%(processName)s[%(process)s]: %(name)s: %(message)s" )
	syslog_handler.setFormatter ( formatter )
	root_logger = logging.getLogger ()
	root_logger.addHandler ( syslog_handler )
	if level is not None:
		root_logger.setLevel ( level )
