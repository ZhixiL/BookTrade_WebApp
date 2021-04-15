#This Program Sets up the SQLite3 Database
#Function - Solely for adding info to database for testing purpose.
# --- by Zhixi Lin ---
import sqlite3
from app import wadb, Account, Post, Buyorder
import datetime
import time
wadb.create_all() #create the database.

#create Account, use the following template & fill it with info you want:
#acc = Account(lastname = "last", firstname = "first", username = "test", password = "pass", email = "test@my.fsu.edu", fsuid = "testid")
#wadb.session.add(acc) #add the account into database
#wadb.session.commit() #commit these added user into the database.


zack = Account(lastname = "Lin", firstname = "Zhixi", username = "zacklin", 
    password = "linzhixi", email = "zl19@my.fsu.edu", fsuid = "zl19")
test1 = Account(lastname = "last1", firstname = "first1", username = "test1", 
    password = "password", email = "test1@my.fsu.edu", fsuid = "test1")
test2 = Account(lastname = "last2", firstname = "first2", username = "test2", 
    password = "password", email = "test2@my.fsu.edu", fsuid = "test2")
test3 = Account(lastname = "last3", firstname = "first3", username = "test3", 
    password = "password", email = "test3my.fsu.edu", fsuid = "test3")
test4 = Account(lastname = "last4", firstname = "first4", username = "test4", 
    password = "password", email = "test4@my.fsu.edu", fsuid = "test4")

wadb.session.add(zack)
wadb.session.add(test1)
wadb.session.add(test2)
wadb.session.add(test3)
wadb.session.add(test4)
wadb.session.commit() 

post2 = Post(by = "zacklin", bookname = "Textbook2", author = "name1",
    price = 10.25, college = "College of Arts and Sciences", description = "This is a sample book", time = datetime.datetime.now())
time.sleep(3)
post1 = Post(by = "zacklin", bookname = "Textbook1", author = "name2",
    price = 11.25, college = "College of Arts and Sciences", description = "This is a sample book", time = datetime.datetime.now())
time.sleep(3)
post4 = Post(by = "test1", bookname = "Textbook4", author = "name1", 
    price = 17.50, college = "College of Arts and Sciences", description = "This is a sample book", time = datetime.datetime.now())
time.sleep(3)
post3 = Post(by = "zacklin", bookname = "Textbook3", author = "name3", 
    price = 8.25, college = "College of Business", description = "This is a sample book", time = datetime.datetime.now())

wadb.session.add(post1)
wadb.session.add(post2)
wadb.session.add(post3)
wadb.session.add(post4)
wadb.session.commit()
