#!/usr/bin/python

from manager_libs import *

def printHelp():
    print "You need help"
    quit()

#Check if running as root
if os.getuid() != 0:
	print "You must run this as root"
	quit()

#Check if proper number of arguments given
numArgs = len(sys.argv)
if numArgs < 3:
    printHelp()


#Create user if first argument is -c
if sys.argv[1] == "-c":
    for i in range(2,numArgs):
		user = sys.argv[i]	
		if not checkUser(user):
			userCreate(user)
		else:
			print "User: '" + user + "' already exisits!"

#Remove user if first  argument is -r
elif sys.argv[1] == "-r":
    for i in range(2,numArgs):
		user = sys.argv[i]
		if checkUser(user):
			userRemove(user)
		else:
			print "User: '" + user + "' does not exisit!"

#If first argument is neither -c nor -r, print help and quit
else:
    printHelp()

