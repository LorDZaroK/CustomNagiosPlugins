# CustomNagiosPlugins
Custom Nagios Plugins for different purposes.


check_teldat_coverage_optparse.py
Old plugin that checks coverage of Teldat 3g equipment measured in dBm. Status strings available in four languages: English, Deutsch, Catalan and Spanish.

Usage:

Nagios command definition:

# TELDAT COVERAGE
define command{
        command_name    check_teldat_coverage
        command_line    $USER1$/check_teldat_coverage.py -H $HOSTADDRESS$ -i $ARG1$ -C $ARG2$ -l $ARG3$
        }
