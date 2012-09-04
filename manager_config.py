
#Location where the database is hosted.
DB_HOST = 'localhost'

#Port for hosted database
DB_PORT = '3306'

#Database user. Must have privillages to add users and create databases. (Root user)
DB_USER = 'root'

#Database password for specified database user.
DB_PASS = ''

#Name to give a user's default database. (username+db_suffix)
DB_SUFFIX = '_main'

#Password salt for linux password.
PASSWORD_SALT = ''

#Group to create. New users will be added to this group.
USER_GROUP = 'hostedusers'

#Default shell to give to newly created users.
USER_SHELL = '/bin/bash'

#Directory to copy public_html files given to new users.
PUBLIC_HTML_TEMPLATE = '/root/public_html_template/'
