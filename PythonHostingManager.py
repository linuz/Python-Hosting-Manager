#!/usr/bin/python
import manager_libs
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
if numArgs != 3:
    printHelp()
else:
	user = sys.argv[2]
	check = checkUser(user)

#Create user if first argument is -c
if sys.argv[1] == "-c":
	if not check:
		if not checkDatabase(user):
			password = getPassword()
			userCreate(user, password)
		else:
			print "Database name: '" + user + manager_libs.DB_SUFFIX + "' already exists!"
	elif check == 2:
		print "User: '"+user+"' already exists!"

#Remove user if first argument is -r
elif sys.argv[1] == "-r":
	if check == 2:
		userRemove(user)
	elif check == 0:
		print "User: '"+user+"' does not exists!"

#If first argument is neither -c nor -r, print help and quit
else:
    printHelp()

