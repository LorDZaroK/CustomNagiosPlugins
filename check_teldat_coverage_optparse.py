#!/usr/bin/python
import sys, subprocess
from optparse import OptionParser
from pysnmp.entity.rfc3413.oneliner import cmdgen

# 24/04/2015

# Arguments
parser = OptionParser(description='Plugin for Nagios. Obtains mobile coverage value from a Teldat Router by SNMP OID and displays it in text and value (dBm). Also displays performance data. Available in 4 languajes: Catala, Castellano, English, Deutsch.')

parser.add_option('-d', '--debug', type = int, help = 'Displays debug info, requires debug coverage value ex: -100')
parser.add_option('-H', '--host', help = 'Target host')
parser.add_option('-i', '--interface', help = 'Target host interface SNMP description')
parser.add_option('-C', '--community', help = 'SNMP Community')
parser.add_option('-l', '--languaje', choices = ['cat', 'esp', 'en', 'de'], help = 'String languaje cat:Catala, esp:Castellano, en:English, de:Deutsch', default='cat')
parser.add_option('-c', '--cacti', action = 'store_true', help = 'Displays raw coverage value for Cacti data input')
(options, args) = parser.parse_args()

if options.host is None:
	parser.error ('Host is mandatory (-H HOST --host HOST)')
	sys.exit(3)

if options.community is None:
        parser.error ('SNMP Community is mandatory (-C COMMUNITY --community COMMUNITY)')
        sys.exit(3)

if options.interface is None:
        parser.error ('Interface is mandatory (-i INTERFACE --interface INTERFACE)')
        sys.exit(3)

host = options.host
community = options.community
lang = options.languaje
interface = options.interface
	
# Debug
if options.debug:
	subprocess.call(['clear'], shell=True)
	print "DEBUG"
	debCoverage = options.debug
	print 'Host: %s\nCommunity: %s\nLanguaje: %s\n\nInterface (Argument): %s' % (host, community, lang, interface)

# SNMP - Fetch coverage
ifdescr = '1.3.6.1.2.1.2.2.1.2'

cmdGen = cmdgen.CommandGenerator()

try:
	ifdescrValue = cmdGen.nextCmd(cmdgen.CommunityData(community), cmdgen.UdpTransportTarget((host, 161)), ifdescr)
	ifdescrValueString = ifdescrValue
except:
	print 'SNMP ERROR'
	sys.exit(3)

for ifaces in ifdescrValueString[3]:
	if ifaces [0][1] == interface:
		ifindex = ifaces [0][0][-1]
		if options.debug:
			print 'SNMP IfDescr: %s\nSNMP IfIndex: %s\nSNMP IfDescr OID: %s' % (ifaces[0][1], ifindex, ifaces[0][0])

oid = '1.3.6.1.4.1.2007.4.1.2.2.2.18.3.2.1.10.%s' % ifindex

try:
	oidvalue = cmdGen.getCmd(cmdgen.CommunityData(community), cmdgen.UdpTransportTarget((host, 161)), oid)
	coverage = oidvalue[3][0][1]
except:
	print 'SNMP ERROR'
	sys.exit(3)

if options.debug:
	print 'SNMP Coverage OID: %s' % oid
	print 'SNMP Coverage value: %s\nDebug coverage value (Argument): %s' % (coverage, debCoverage)
	coverage = debCoverage
	print 'New coverage value (Debug argument): %s\n\nScript return:' % coverage

# Cacti output
if options.cacti:
	print coverage
	sys.exit(3)

# Language strings
if lang == 'cat':
	woCoverage = 'Sense cobertura'
	vlowCoverage = 'Cobertura molt baixa'
	lowCoverage = 'Cobertura baixa'
	gdCoverage = 'Bona cobertura'
	vgdCoverage = 'Molt bona cobertura'
	exCoverage = 'Cobertura excel.lent'

elif lang == 'esp':
	woCoverage = 'Sin cobertura'
        vlowCoverage = 'Cobertura muy baja'
        lowCoverage = 'Cobertura baja'
        gdCoverage = 'Buena cobertura'
        vgdCoverage = 'Muy buena cobertura'
        exCoverage = 'Cobertura excelente'

elif lang == 'en':
        woCoverage = 'Without coverage'
        vlowCoverage = 'Very low coverage'
        lowCoverage = 'Low coverage'
        gdCoverage = 'Good coverage'
        vgdCoverage = 'Very good coverage'
        exCoverage = 'Excellent coverage'

elif lang == 'de':
        woCoverage = 'Ohne Netzabdeckung'
        vlowCoverage = 'Sehr schwache Netzabdeckung'
        lowCoverage = 'Schwache Netzabdeckung'
        gdCoverage = 'Gute Netzabdeckung'
        vgdCoverage = 'Sehr gute Netzabdeckung'
        exCoverage = 'Exzellente Netzabdeckung'

# Displaying coverage information
if coverage <= -113:
	print 'CRITICAL - %s: %s dBm | %s' % (woCoverage, coverage, coverage)
	sys.exit(2)
elif coverage > -113 and coverage <= -111:
	print 'CRITICAL - %s: %s dBm | %s' % (vlowCoverage, coverage, coverage)
	sys.exit(2)
elif coverage > -111 and coverage <= -97:
	print 'WARNING - %s: %s dBm | %s' % (lowCoverage, coverage, coverage)
	sys.exit(1)
elif coverage > -97 and coverage <= -87:
	print 'OK - %s: %s dBm | %s' % (gdCoverage, coverage, coverage)
	sys.exit(0)
elif coverage > -87 and coverage <= -71:
	print 'OK - %s: %s dBm | %s' % (vgdCoverage, coverage, coverage)
	sys.exit(0)
elif coverage > -71:
	print 'OK - %s: %s dBm | %s' % (exCoverage, coverage, coverage)
	sys.exit(0)
else:
	print 'UNKNOWN'
	sys.exit(3)
