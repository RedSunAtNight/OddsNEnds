#! usr/bin/env python

# compareTimes.py
# @author RedSunAtNight
# Written really for my own use. Runs just fine on Ubuntu 12.04.
# Requirements: time (http://manpages.ubuntu.com/manpages/lucid/man1/time.1.html)
# Lets you compare the running times of programs.
# The programs whose times are to be compared are entered as command-line arguments.
# The variable called iterations tells you how many times to run each. The running times for each program are averaged.

import subprocess
import sys
import re
from pprint import pprint

timesDict = {}
iterations = 100

# regular expressions that will be used later
realExp = re.compile(r'(real.[0-9]+\.[0-9]+)')
userExp = re.compile(r'(user.[0-9]+\.[0-9]+)')
sysExp = re.compile(r'(sys.[0-9]+\.[0-9]+)')
justnums = re.compile(r'[0-9]+\.[0-9]+')
# go through all args. Ignore the one that starts this program.
for item in sys.argv[1:]:
	timesDict[item] = {'real':0.0, 'user':0.0, 'sys':0.0}
	for i in range(0, iterations):
		# time the program
		runner = subprocess.Popen('time -p python {0}'.format(item), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(out, err) = runner.communicate() # stderr will have the output of time
		#print 'output: \n', out, '\n'
		#print 'error: \n', err, '\n'
		# separate the times
		mreal = realExp.search(str(err))
		muser = userExp.search(str(err))
		msys = sysExp.search(str(err))
		# if at least one doesn't exist, there is a problem
		if (not mreal or not muser or not msys):
			raise RuntimeError('Time not reported for program {0}, iteration {1}'.format(item, i))
		
		# real - separate out the actual time from the label
		subreal = mreal.group()
		numsreal = re.search(justnums, subreal)
		realtime = numsreal.group()
		timesDict[item]['real'] += float(realtime)
		# user - separate out the actual time from the label
		subuser = muser.group()
		numsuser = re.search(justnums, subuser)
		usertime = numsuser.group()
		timesDict[item]['user'] += float(usertime)
		# sys - separate out the actual time from the label
		subsys = msys.group()
		numssys = re.search(justnums, subsys)
		systime = numssys.group()
		timesDict[item]['sys'] += float(systime)

	# Now that the times are all added together, time to get the average
	for key in timesDict[item]:
		timesDict[item][key] /= iterations

pprint(timesDict)
