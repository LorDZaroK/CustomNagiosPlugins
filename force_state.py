#!/usr/bin/python

# This script forces a nagios dummy state for testing purposes without interfering the monitorization of real host and services.
# Usage: NAGIOSPATH/libexec/force_state.py -s STATE (ok, warning, critical or unknown)
# Nagios command:
#	define command{
#   	     command_name    force_state
#       	 command_line    /usr/local/nagios/libexec/force_state.py -s $ARG1$
#	}
#
# Nagios definition example (forcing a warning state):
#	# =============================================================================
#	# ===== 2. DummyHost_WARNING
#	# =============================================================================
#
#	define host{
#		use					  	generic-switch
#		host_name			  	DummyHost_WARNING
#		alias				  	Dummy Hosts forced state WARNING
#		address				  	127.0.0.1
#		hostgroups			  	Testgroup
#		normal_check_interval     60
#		retry_check_interval      60
#	}
#
#	define service{
#		use                     generic-service
#		host_name				DummyHost_WARNING
#		service_description     Dummy service forced to WARNING
#		check_command           force_state!warning
#		servicegroups			sg-testgroup
#		normal_check_interval   60
#		retry_check_interval    60
#	}
#
# Created by Albert Casas
# Version 1.0 - 22/10/2015

import sys
from optparse import OptionParser

# Arguments
parser = OptionParser(description='Plugin for Nagios. Force a state for testing purposes.')

parser.add_option('-s', '--state', choices = ['ok', 'warning', 'critical', 'unknown'], help = 'Select a state to force: ok, warning, critical or unknown', default='ok')
(options, args) = parser.parse_args()

if options.state == 'ok':
	print "Forced dummy state: OK"
	sys.exit(0)
elif options.state == 'warning':
	print "Forced dummy state: WARNING"
	sys.exit(1)
elif options.state == 'critical':
	print "Forced dummy state: CRITICAL"
	sys.exit(2)
elif options.state == 'unknown':
	print "Forced dummy state: UNKNOWN"
	sys.exit(3)
else:
	print "Invalid option"
	sys.exit(3)