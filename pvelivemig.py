#!/usr/bin/python

import subprocess
import platform
import itertools
import sys

nodename = platform.node()
nodelist = subprocess.Popen("pvesh ls nodes|awk '{print $2}'", stdout=subprocess.PIPE, shell=True).stdout.read().split('\n')
nodelist.pop()
nodelist.remove(nodename)
for node in nodelist:
	statuscmd = "pvesh get nodes/" + node + "/status"
	try:
		subprocess.check_call(statuscmd.split(" ") , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	except subprocess.CalledProcessError:
		nodelist.remove(node)

print "nodelist = ", nodelist

commandvms = "pvesh ls nodes/" + nodename + "/qemu |awk '{print $2}'"
vmlist = subprocess.Popen(commandvms, stdout=subprocess.PIPE, shell=True).stdout.read().split('\n')
vmlist.pop()
print "vmlist = ", vmlist


for vm,node in itertools.izip(vmlist,itertools.cycle(nodelist)):
	migcommand = "qm migrate %s %s -online" % (vm,node)
	print migcommand
	#subprocess.Popen(migcommand, stdout=subprocess.PIPE, shell=True).stdout.read())
	subprocess.call(migcommand, shell=True)


