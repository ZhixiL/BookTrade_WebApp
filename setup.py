#This Program Sets up the SQLite3 Database
#Function - Solely for adding info to database for testing purpose.
# --- by Zhixi Lin ---
import sqlite3
from app import wadb, Account, Post
import datetime
import time
wadb.create_all() #create the database.

#create Account, use the following template & fill it with info you want:
#acc = Account(lastname = "last", firstname = "first", username = "test", password = "pass", email = "test@my.fsu.edu", fsuid = "testid")
#wadb.session.add(acc) #add the account into database
#wadb.session.commit() #commit these added user into the database.


