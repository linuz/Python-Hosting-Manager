#!/usr/bin/python

import os, sys

def printHelp():
    print "You need help"
    quit()

def checkUser(username):
	print "Checking if user: '" + username + "' already exisits..."
	file = open("/etc/passwd","r")
	for line in file:
		if username+":" in line:
			file.close()
			return 1	
	file.close()
	return 0

def userCreate(username):
	os.system("useradd " + username)
	os.system("chmod 711 /home/" + username)
	os.system("mkdir /home/" + username + "/public_html")
	os.system("chmod 711 /home/" + username + "/public_html")
	os.system("cp -rf /root/public_html_template/* /home/" + username + "/public_html/")
	print "User: '" + username + "' has been created!"

def userRemove(username):
	confirmationString = "Are you sure you want to delete "+username +"? (Type in 'yes'): "
	if raw_input(confirmationString) == "yes":	
		os.system("userdel --remove " + username)
		print username + " has been deleted"
	else:
		print "Deletion of user: '" + username + "' has been aborted"

numArgs = len(sys.argv)
if numArgs < 3:
    printHelp()

if sys.argv[1] == "-c":
    for i in range(2,numArgs):
		user = sys.argv[i]	
		if not checkUser(user):
			userCreate(user)
		else:
			print "User: '" + user + "' already exisits!"
elif sys.argv[1] == "-r":
    for i in range(2,numArgs):
		user = sys.argv[i]
		if checkUser(user):
			userRemove(user)
		else:
			print "User: '" + user + "' does not exisit!"
else:
    printHelp()

