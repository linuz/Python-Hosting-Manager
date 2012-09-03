#!/usr/bin/python
import manager_libs
from manager_libs import *

def printHelp():
	print "You need help"
	print "USAGE: sudo ./Python-Hosting-Manager.py <option> <username>"
	print "\t-c\tCreate User\n\t-r\tRemove User"
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

#Create user if first argument is -c
if sys.argv[1] == "-c":
	userCheck = checkUser(user)
	if userCheck == 0:
		dbCheck = checkDatabase(user)
		if dbCheck == 0:
			password = getPassword()
			userCreate(user, password)
		elif dbCheck == 1:
			print "Database user: '"+user+"' already exists!" 
		elif dbCheck == 2 :
			print "Database: '" + user + manager_libs.DB_SUFFIX + "' already exists!"
	elif userCheck == 2:
		print "User: '"+user+"' already exists!"

#Remove user if first argument is -r
elif sys.argv[1] == "-r":
	userCheck = checkUser(user)
	if userCheck == 2:
			userRemove(user)
	elif userCheck == 0:
		print "User: '"+user+"' does not exists!"

#If first argument is neither -c nor -r, print help and quit
else:
    printHelp()

