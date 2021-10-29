"""

This would be the temporary database file.

"""

import sqlite3

#initialize db file
DB_FILE = "database.db"

#connect db
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#create tables for database
command = "CREATE TABLE"

# Creating table with username | password | stories contributed table
c.execute (command + "user_info (username TEXT, password TEXT, stories_contributed TEXT)")

# creating table with story title | user contributed | story entry
c.execute (command + "story (title TEXT, user TEXT, entry TEXT)")


def write_to_story(title, user_contributed, entry):
    contributor = ""
    entry = ""
    c.execute ("INSERT INTO story VALUES(?, ?,?)", title, contributor, entry)

    #c.execute("SELECT ")
