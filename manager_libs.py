import os, sys

#Check in /etc/passwd if the specified users exisit. Returns 1 if exists, 0 if not.
def checkUser(username):
    print "Checking if user: '" + username + "' already exisits..."
    file = open("/etc/passwd","r")
    for line in file:
        if username+":" in line:
            file.close()
            return 1
    file.close()
    return 0

#Creates user using os.system commands. Also makes directories and files.
def userCreate(username):
    os.system("useradd " + username)
    os.system("chmod 711 /home/" + username)
    os.system("mkdir /home/" + username + "/public_html")
    os.system("chmod 711 /home/" + username + "/public_html")
    os.system("cp -rf /root/public_html_template/* /home/" + username + "/public_html/")
    print "User: '" + username + "' has been created!"

#Removes user using os.system commands.
def userRemove(username):
    confirmString = "Are you sure you want to delete "+username +"? (Type in 'yes'): "
    if raw_input(confirmString) == "yes":
        os.system("userdel --remove " + username)
        print "User: " + username + " has been deleted!"
    else:
        print "Deletion of user: '" + username + "' has been aborted"

