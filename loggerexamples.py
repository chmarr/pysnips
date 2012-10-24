import logging, logging.handlers, os

def logging_basic_syslog ( facility="user", level=logging.WARNING ):
	if os.path.exists ( "/dev/log" ):
		path = "/dev/log"
	elif os.path.exists ( "/var/run/syslog" ):
		path = "/var/run/syslog"
	else:
		path = ( 'localhost', logging.handlers.SysLogHandler.SYSLOG_UDP_PORT )

	syslog_handler = logging.handlers.SysLogHandler ( path )
	# TODO: on OS/X processName ends up as "MainProcess" rather than argv[0]
	formatter = logging.Formatter ( "%(processName)s[%(process)s]: %(name)s: %(message)s" )
	syslog_handler.setFormatter ( formatter )
	root_logger = logging.getLogger ()
	root_logger.addHandler ( syslog_handler )
	root_logger.setLevel ( level )
