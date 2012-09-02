import crypt
import getpass
import os
import sys
import subprocess as sp

#Database credentials. TODO: implement config file!
DB_USER = ''
DB_PASS = ''
DB_SUFFIX = "_main"
PASSWORD_SALT = "kv"

#Check in /etc/passwd if the specified users exisit. Returns 1 if exists, 0 if not.
def checkUser(user):
	print "Checking if user: '"+user+"' already exisits..."
	file = open("/etc/passwd","r")
	for line in file:
		if user+":" in line:
			file.close()
			return 1
	file.close()
	print "User does not already exisit. Creating user..."
	return 0

#Check if new user's database already exisits
def checkDatabase(user):
	mysql_check = sp.Popen("mysql --user="+DB_USER+" --password="+DB_PASS+" -e 'SHOW DATABASES;'", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
	mysql_out, mysql_err = mysql_check.communicate()
	if user+DB_SUFFIX in mysql_out:
		return 1
	else:
		return 0

#Grab and encrypt password
def getPassword():
	while True:
		password1 = getpass.getpass("New Password: ")
		password2 = getpass.getpass("Confirm Password: ")
		if not password1 == password2:
			print "Passwords do not match! Try again:"
		else:
			break
	return password1

#Creates user using os.system commands. Also makes directories and files.
def userCreate(user, password, shell):
    encPass = crypt.crypt(password, PASSWORD_SALT)
    os.system("useradd --create-home --shell "+shell+" --password "+encPass+" "+user)
    os.system("chmod 711 /home/"+user)
    os.system("mkdir /home/"+user+"/public_html")
    os.system("chown -R "+user+":"+user+" /home/"+user+"/public_html")
    os.system("chmod 711 /home/"+user+"/public_html")
    os.system("cp -rf /root/public_html_template/* /home/"+user+"/public_html/")
    os.system("mysql --user="+DB_USER+" --password='"+DB_PASS+"' -e \"CREATE DATABASE "+user+DB_SUFFIX+"; GRANT ALL ON "+user+DB_SUFFIX+".* TO '"+user+"' IDENTIFIED BY '"+password+"'; FLUSH PRIVILEGES;\"")
    print "User: '"+user+"' has been created!"

#Removes user using os.system commands.
def userRemove(user):
    confirmString = "Are you sure you want to delete "+user +"? (Type in 'yes'): "
    if raw_input(confirmString) == "yes":
        os.system("userdel --remove " + user)
        os.system("mysql --user="+DB_USER+" --password='"+DB_PASS+"' -e \"DROP DATABASE "+user+DB_SUFFIX+"; DROP USER "+user+"; FLUSH PRIVILEGES;\"")
        print "User: " + user + " has been deleted!"
    else:
        print "Deletion of user: '" + user + "' has been aborted"


