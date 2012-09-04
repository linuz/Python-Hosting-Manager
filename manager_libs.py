import crypt
import getpass
import hashlib
import os
import re
import sys
import subprocess as sp
import manager_config
import MySQLdb as mysql
from manager_config import *

#Ecrypt password into MySQL Algorithm. (MySQL 4.1 >= 5.1)
def mysqlEncPass(password):
	password = hashlib.sha1(password).digest()
	password = hashlib.sha1(password).hexdigest()
	password = password.upper()
	password = "*"+password
	return password
	
#Check in /etc/passwd if the specified users exisit. Returns 1 if exists, 0 if not.
def checkUser(user):
	user = user.lower()
	if not re.match("^[A-Za-z0-9_-]*$", user) or len(user) > 20:
		print "Name is invalid!"	
		return 1
	print "Checking if user: '"+user+"' already exisits..."
	file = open("/etc/passwd","r")
	for line in file:
		if user+":" in line:
			file.close()
			return 2
	file.close()
	return 0

#Check if new user or database already exisits
def checkDatabase(user):
	con = mysql.connect(DB_HOST,DB_USER,DB_PASS)
	cur = con.cursor()
	userCheck_query = "SELECT user FROM mysql.user WHERE user='"+user+"';"
	dbCheck_query = "SHOW DATABASES;"
	cur.execute(userCheck_query)
	mysql_out = cur.fetchall()
	if mysql_out:
		con.close()
		return 1
	mysql_out = cur.execute(dbCheck_query)
	mysql_out = cur.fetchall()
	for s in mysql_out:
		if s[0] == user+DB_SUFFIX:
			con.close()
			return 2
	con.close()
	return 0

#Grab and encrypt password. Also enforces password policy.
def getPassword():
	passMatch = 0
	for i in range(0,3):
		password1 = getpass.getpass("New Password: ")
		if not password1:
			print "Password cannot be blank!"
			continue
		password2 = getpass.getpass("Confirm Password: ")
		if not password1 == password2:
			print "Passwords do not match! Try again:"
		else:
			passMatch = 1
			break
	if passMatch:
		return password1
	else:
		print "User creation aborted"
		quit()

#Creates user using os.system commands. Also makes directories and files.
def userCreate(user, password):
	encPass = crypt.crypt(password, PASSWORD_SALT)
	mysqlPass = mysqlEncPass(password)
	con = mysql.connect(DB_HOST,DB_USER,DB_PASS)
	cur = con.cursor()
	mysqlQuery = "CREATE DATABASE "+user+DB_SUFFIX+"; GRANT ALL ON "+user+DB_SUFFIX+".* TO '"+user+"' IDENTIFIED BY PASSWORD '"+mysqlPass+"'; FLUSH PRIVILEGES;"
	cur.execute(mysqlQuery)
	mysql_out = cur.fetchall()
	if mysql_out:
		print mysql_out
	os.system("useradd --create-home --shell "+USER_SHELL+" --groups " +USER_GROUP+" --password "+encPass+" "+user)
	os.system("chmod 711 /home/"+user)
	os.system("mkdir /home/"+user+"/public_html")
	os.system("chown -R "+user+":"+user+" /home/"+user+"/public_html")
	os.system("chmod 711 /home/"+user+"/public_html")
	os.system("cp -rf "+PUBLIC_HTML_TEMPLATE+"* /home/"+user+"/public_html/")
	print "User: '"+user+"' has been created!"

#Removes user using os.system commands.
def userRemove(user):
    confirmString = "Are you sure you want to delete "+user +"? (Type in 'yes'): "
    if raw_input(confirmString) == "yes":
		con = mysql.connect(DB_HOST,DB_USER,DB_PASS)
		cur = con.cursor()
		mysqlQuery = "DROP DATABASE "+user+DB_SUFFIX+"; DROP USER "+user+"; FLUSH PRIVILEGES;"
		cur.execute(mysqlQuery)
		mysql_out = cur.fetchall()
		if mysql_out:
			print mysql_out
		os.system("userdel --remove " + user)
		print "User: " + user + " has been deleted!"
    else:
        print "Deletion of user: '" + user + "' has been aborted"
