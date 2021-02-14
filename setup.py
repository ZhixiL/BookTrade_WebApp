#This Program Sets up the SQLite3 Database
import sqlite3

revdb = sqlite3.connect('webapp.db')
print ("Opened webapp.db databse successfully!")
revdb.close()