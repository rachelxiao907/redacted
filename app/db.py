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

# add to existing stories kind of works for now
def add_to_story(title, contributor, entry):

    """
    add_to_story would add entries and contributors of the entry to story database
    also add this story to the list of stories that the user stories_contributed
    returns nothing

    As of now it would add to the story every time the command is called, re running won't
    clear the database

    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # creates a dictionary to facilitate argument passing in the future
    dict = {"title":title, "contributor":contributor, "entry": entry}
    #print(dict)

    # get the contributor and entry from the current story
    command = "SELECT contributor, entry FROM story WHERE title=:title"
    c.execute(command, dict) # the field in dict would replace :title
    contributor_entry_list = c.fetchall() #stores the information. It's a list of tuple, so kind of like 2D array
    #print(contributor_entry_list)

    # add new information to contributor and entry through string concatenation, separated with \n
    #print(contributor_entry_list)
    entry = contributor_entry_list[0][1] + "\n" + entry
    contributor = contributor_entry_list[0][0] + "\n" + contributor

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



def get_story (title):
    """
    get_story gets the entire story, returns the story entries and the different
    users that contributed to each entry in a list
    [contributors_list, story_entry_list]
    Yuqing will code this part but Rachel should check since she's using it for the
    past story part in /home page
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
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
    #print(get_story.__doc__)
    return output_list



def get_story_last_entry (title):

    """
    get_story_last_entry gets the last entry for a story, returns
    the user contributed to the last entry and the last entry in a list
    [contributor, last_entry]

    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # use get_story in its implementation
    output_list = []
    big_list = get_story(title)
    for i in range(2):
        output_list.append(big_list[i][-1])
    return output_list


def get_story_addable(username):

    """
    This would get the stories that the user did not contribute to,
    these are the stories that they can add to on the /add page

    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #titles of all stories, each title in a tuple
    c.execute("SELECT title FROM story")
    titles = c.fetchall()

    #uncomment when get_stories_contributed done
    #stories_contributed = get_stories_contributed(username)

    #for testing
    stories_contributed = ["story1"]

    addable_stories = []

    #if a story is not in stories_contributed, it's addable
    for i in titles:
        if ((i[0] in stories_contributed) == False):
            addable_stories.append(i[0])

    return addable_stories

"""
# -- testing add_to_story, get_story, get_story_last_entry --

c.execute ("INSERT INTO story VALUES ('story1', 'user1', 'entry1')")
c.execute ("INSERT INTO story VALUES ('story2', 'user1', 'entry1')")
c.execute ("INSERT INTO story VALUES ('story3', 'user1', 'entry1')")
#c.execute ("INSERT INTO user_info VALUES ('user1', 'pass1', 'story1')")

#because we are doing a connenct for every function, make sure initial test cases are saved
db.commit()
"""

"""
# add_to_story test
add_to_story("story1", "user2", "world")


#get_story test
print (get_story('story1'))

#get story last entry test
print(get_story_last_entry("story1"))

#print(get_story.__doc__)

print (get_story_addable("user1"))
"""

"""
def add_login(username, password):
    """
    add_login would be used for creating account

    """

    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print(username)
    command = "INSERT INTO user_info VALUES(?, ?, ?)"
    c.execute(command, (username, password, "")) # add u/p pair to database, leave stories contributed blank for now
    db.commit() # commit changes to db


def get_login(username, password):
    """
    get_login would get password to flask for checking

    """
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


#def get_stories_contributed (username):
    """
    get_stories_contributed would return the list of stories that
    the user contributed
    Rachel will do this and determine what exactly it returns, whether it's the
    titles and then call get_story or the entire thing is ready for flask
    """


# def add_stories_contributed (title):
    """
    add_stories_contributed would add this story to the list of
    stories that the user had contributed.
    We can technically do it in add_to_story but I feel like
    it's easier to split up work if it's this way
    Rachel will do this
    """
    #db.commit()

#def create_story(title, entry, user):

    """

    For the /create page, add a new story to the story table

    Rachel will do

    """
    #db.commit()


#db.close() # this should go at the very end of init.py, remember to import db into init.py
