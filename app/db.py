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
command = "CREATE TABLE "

# Creating table with username | password | stories contributed table
c.execute (command + "user_info (username TEXT, password TEXT, stories_contributed TEXT)")

# creating table with story title | user contributed | story entry
c.execute (command + "story (title TEXT, contributor TEXT, entry TEXT)")

#testing
c.execute ("INSERT INTO story VALUES('story1', 'user1', 'hello')")

#doesn't work yet
def write_to_story(_title, _contributor, _entry):
    contributor = ""
    entry = ""
    #c.execute ("INSERT INTO story VALUES(?, ?,?)", _title, _contributor, _entry)

    c.execute("SELECT contributor FROM story WHERE title = _title")
    contributor_list = c.fetchall()
    print(contributor_list)

write_to_story("story1", "user2", "world")
