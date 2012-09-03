Python-Hosting-Manager
======================

NEEDS A BETTER NAME!

Web services hosting manager for python.

I am writing this to make it easier for anyone to create new accounts for their friends who also want access to their server for webhosting reasons.

Currently, this program will do the following:

1) Specify an option and a username (See usage)

2) If you choose '-c', it will check the /etc/passwd file if the username already exists. It will then check to see if a database or database user exists with the same name.

3) If none exists, it will ask for a password, then it will create the user account using useradd, copy the public_html folder from whatever is in the config to their home directory and chmod the proper permissions

4) It will now create a database user and a database name with the user and db_prefix variable in the config. User will have all permissions to that one database.

5) Now if you choose '-r', it will completely reverse all these changes. Removes database, database user, linux user, and home directory.

USAGE:
=======
Elevated privillages is required!

sudo ./Python-Hosting-Manager.py <option> <username>
	-c		Create user
	-r		remove user

TODO:
======
* Create a setup and pre-req check script.
* Create a database backend to store logs and user information.
* Create a front end web interface for users to log into and manage their account. (Look into Django)
* Allow users to manage and create new databases from web interface.

CHANGES:
=========

*Added username length verification. Will not take usernames greater than 20 characters.

*Will now add newly created users to a group specified in the config file.

*Will now properly check if database user already exisits and/or a database with the same name already exisits before creating a user.

*Program will terminate upon 3 incorrect password comaperisons.

*Now hashes MySQL User passwords before being sent to queries.

*All Constant variables now in manager_config.py file.

*Usernames are now validated before passing into command.

*Now creates a database user and database for new account.
