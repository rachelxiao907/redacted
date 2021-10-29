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
command = "CREATE TABLE "

# Creating table with username | password | stories contributed table
c.execute (command + "user_info (username TEXT, password TEXT, stories_contributed TEXT)")

# creating table with story title | user contributed | story entry
c.execute (command + "story (title TEXT, contributor TEXT, entry TEXT)")

#testing
#c.execute ("INSERT INTO story VALUES ('story1', 'user1', 'entry1')")

# add to existing stories kind of works for now, Yuqing
def add_to_story(_title, _contributor, _entry):
    contributor = ""
    entry = ""

    # creates a dictionary to facilitate argument passing in the future
    dict = {"title":_title, "contributor":contributor, "entry": entry}

    # get the contributor and entry from the current story
    command = "SELECT contributor, entry FROM story WHERE (title=:title)"
    c.execute(command, dict) # the field in dict would replace :title
    contributor_entry_list = c.fetchall() #stores the information. It's a list of tuple, so kind of like 2D array

    # add new information to contributor and entry through string concatenation, separated with \n
    entry += contributor_entry_list[0][1] + "\n" + _entry
    contributor += contributor_entry_list[0][0] + "\n" + _contributor

    # reset the dictionary to contain the most recent information
    dict['contributor'] = contributor
    dict['entry'] = entry

    #updates the database with the new dictionary
    c.execute("UPDATE story SET contributor = :contributor WHERE title =:title", dict)
    c.execute("UPDATE story SET entry = :entry WHERE title =:title", dict)

    #testing pritn statement
    command = "SELECT * FROM story WHERE (title=:title)"
    c.execute(command, dict)
    print(c.fetchall())

    # to be added: parts about marking this story as contributed by the user
    # add_stories_contributed (_title)

# add_to_story test
#add_to_story("story1", "user2", "world")

"""
get_story gets the entire story, returns the story entries and the different
users that contributed to each entry in a list
[contributors_list, story_entry_list]

Yuqing will code this part but Rachel should check since she's using it for the
past story part in /home page

"""
#def get_story (title):


"""
get_story_last_entry gets the last entry for a story, returns
the user contributed to the last entry and the last entry in a list
[contributor, last_entry]

Yuqing will do this

"""
# def get_story_last_entry (title):
    # will use get_story in its implementation

"""
add_login would be used for creating account

Michael will do this

"""
#def add_login(username, password):

"""
get_login would get password to flask for checking

Michael will do this
"""
# def get_login(username):

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


db.commit()
db.close()
