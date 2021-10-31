"""
This would be the database file.
Make sure to comment out the testing parts when you commit to github
"""

import sqlite3

#initialize db file
DB_FILE = "database.db"

#connect db
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#create tables for database
command = "CREATE TABLE IF NOT EXISTS "

# Creating table with username | password | stories contributed table
c.execute (command + "user_info (username TEXT, password TEXT, stories_contributed TEXT, CONSTRAINT uni_user UNIQUE(username))") # vals in username col must be unique

# creating table with story title | user contributed | story entry
c.execute (command + "story (title TEXT, contributor TEXT, entry TEXT)")



'''
# -- testing --
c.execute("INSERT INTO user_info VALUES(?, ?)", ("hi", "bye"))
c.execute("INSERT INTO user_info VALUES(?, ?)", ("hiakjsdhajsdhkajsdgh", "bye"))
try:
    c.execute("INSERT INTO user_info VALUES(?, ?)", ("hi", "aksjdhakd"))
except sqlite3.IntegrityError:
    print("asdhasd")
c.execute("SELECT * from user_info WHERE username=\"hi\"")
print(c.fetchall())
'''

"""
add_to_story would add entries and contributors of the entry to story database
also add this story to the list of stories that the user stories_contributed
returns nothing

As of now it would add to the story every time the command is called, re running won't
clear the database and maybe we should clear the database at the end of init.py so we
always have a new database to work with every time the program is ran.
"""
# add to existing stories kind of works for now
def add_to_story(title, contributor, entry):

    # creates a dictionary to facilitate argument passing in the future
    dict = {"title":title, "contributor":contributor, "entry": entry}
    #print(dict)

    # get the contributor and entry from the current story
    command = "SELECT contributor, entry FROM story WHERE title=:title"
    c.execute(command, dict) # the field in dict would replace :title
    contributor_entry_list = c.fetchall() #stores the information. It's a list of tuple, so kind of like 2D array
    #print(contributor_entry_list)

    # add new information to contributor and entry through string concatenation, separated with \n
    entry = contributor_entry_list[0][1] + "\n" + entry
    contributor = contributor_entry_list[0][0] + "\n" + contributor
    #print(contributor_entry_list)
    #print(contributor)

    # reset the dictionary to contain the most recent information
    dict['contributor'] = contributor
    dict['entry'] = entry
    #print(dict)

    #updates the database with the new dictionary
    c.execute("UPDATE story SET contributor = :contributor WHERE title =:title", dict)
    c.execute("UPDATE story SET entry = :entry WHERE title =:title", dict)

    #testing print statement
    command = "SELECT * FROM story WHERE (title=:title)"
    c.execute(command, dict)
    #print(c.fetchall())

    db.commit()
    # to be added: parts about marking this story as contributed by the user
    # add_stories_contributed (_title)


# add_to_story test
# add_to_story("story1", "user2", "world")

"""
get_story gets the entire story, returns the story entries and the different
users that contributed to each entry in a list
[contributors_list, story_entry_list]
Yuqing will code this part but Rachel should check since she's using it for the
past story part in /home page
"""

def get_story (title):
    #selects contributors and entry
    c.execute("SELECT contributor, entry FROM story WHERE title = :title", {"title":title})
    entry_list = c.fetchall()
    output_list = []

    #index 0 because tuple
    for i in range(2):
        #split for each \n
        output_list.append(entry_list[0][i].split('\n'))

    #diag print statement
    #print(output_list)
    return output_list



"""
get_story_last_entry gets the last entry for a story, returns
the user contributed to the last entry and the last entry in a list
[contributor, last_entry]
Yuqing will do this
"""
def get_story_last_entry (title):
    # use get_story in its implementation
    output_list = []
    big_list = get_story(title)
    for i in range(2):
        output_list.append(big_list[i][-1])
    return output_list

"""
# -- testing add_to_story, get_story, get_story_last_entry -- 

c.execute ("INSERT INTO story VALUES ('story1', 'user1', 'entry1')")

# add_to_story test
add_to_story("story1", "user2", "world")

#get_story test
print (get_story('story1'))

#get story last entry test
print(get_story_last_entry("story1"))
"""


"""
add_login would be used for creating account
Michael will do this
"""
def add_login(username, password):
    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print(username)
    command = "INSERT INTO user_info VALUES(?, ?, ?)"
    c.execute(command, (username, password, "")) # add u/p pair to database, leave stories contributed blank for now
    db.commit() # commit changes to db
"""
get_login would get password to flask for checking
Michael will do this
"""
def get_login(username, password):
    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")" # check if username exists in the db
    c.execute(command)
    data = c.fetchall()
    if(data == []): # no user exists
        return "User Not Found"
    elif(data[0][1] != password): # password is wrong
        return "Username and password do not match"
    else: # we good
        return ""

"""
get_stories_contributed would return the list of stories that
the user contributed
Rachel will do this and determine what exactly it returns, whether it's the
titles and then call get_story or the entire thing is ready for flask
"""
#def get_stories_contributed (username):

"""
add_stories_contributed would add this story to the list of
stories that the user had contributed.
We can technically do it in add_to_story but I feel like
it's easier to split up work if it's this way
Rachel will do this
"""
# def add_stories_contributed (title):
    #db.commit()

"""

For the /create page, add a new story to the story table

Rachel will do

"""
#def create_story(title, entry, user):
    #db.commit()


#db.close() # this should go at the very end of init.py, remember to import db into init.py
