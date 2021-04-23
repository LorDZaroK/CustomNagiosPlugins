# CustomNagiosPlugins
Custom Nagios Plugins for different purposes.

----

### check_teldat_coverage_optparse.py:

Old plugin that checks coverage of Teldat 3g equipment measured in dBm. Status strings available in four languages: English, Deutsch, Catalan and Spanish.

Nagios command definition:
 ```
define command{
        command_name    check_teldat_coverage
        command_line    $USER1$/check_teldat_coverage.py -H $HOSTADDRESS$ -i $ARG1$ -C $ARG2$ -l $ARG3$
        }
```

----

### force_state.py:

This script forces a nagios dummy state for testing purposes without interfering the monitorization of real host and services.

Usage: NAGIOSPATH/libexec/force_state.py -s STATE (ok, warning, critical or unknown)

Nagios command definition:
```
Nagios command:
define command{
  	     command_name    force_state
      	 command_line    /usr/local/nagios/libexec/force_state.py -s $ARG1$
}
```

Nagios host and service definition example (forcing a warning state):
```
# =============================================================================
# ===== 2. DummyHost_WARNING
# =============================================================================
define host{
	use					  	generic-switch
	host_name			  	DummyHost_WARNING
	alias				  	Dummy Hosts forced state WARNING
	address				  	127.0.0.1
	hostgroups			  	Testgroup
	normal_check_interval     60
	retry_check_interval      60
}

define service{
	use                     generic-service
	host_name				DummyHost_WARNING
	service_description     Dummy service forced to WARNING
	check_command           force_state!warning
	servicegroups			sg-testgroup
	normal_check_interval   60
	retry_check_interval    60
}
```
----
