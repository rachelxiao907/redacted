'''
This file contains methods that accesses and add to the database.
'''

import sqlite3

#initialize db file
DB_FILE = "database.db"

#connect db
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#create tables for database
command = "CREATE TABLE IF NOT EXISTS "

# Creating table that contains username | password | stories contributed, usernames must be unique
c.execute (command + "user_info (username TEXT, password TEXT, stories_contributed TEXT, CONSTRAINT uni_user UNIQUE(username))")

# creating table with story title | user contributed | story entry, titles must be unique
c.execute (command + "story (title TEXT type UNIQUE, contributor TEXT, entry TEXT)")

def get_login(username, password):
    """
    Returns the correct error message when the user is logging in.

        Parameters:
            username (str): The username that the user entered
            password (str): The password that the user entered

        Returns:
            "User Not Found": Username does not match any entry in the database
            "Incorrect Password": Username is found in the database but password doesn't match
            "": Username and password matches

    """
    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # check if username exists in the db
    command = f"SELECT * FROM user_info WHERE (username = \"{username}\")"
    c.execute(command)
    data = c.fetchall()

    # no user exists
    if(data == []):
        return "User Not Found"

    # password is wrong
    elif(data[0][1] != password):
        return "Incorrect Password"

    # username and password is correct
    else:
        return ""


def add_login(username, password):
    """
    Creates an account in the database
    Adds a new row for new username and password in user_info table in database

        Parameters:
            username (str): The username that the user entered
            password (str): The password that the user entered

        Returns:
            None
    """

    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # add username and password pair to database, no stories_contributed blank at account creation
    command = "INSERT INTO user_info VALUES(?, ?, ?)"
    c.execute(command, (username, password, ""))

    # commit changes to db
    db.commit()


def create_story(title, user, entry):
    """
    Add a story to the story table in database

        Parameters:
            title (str): The title of the story that the user entered
            user (str): The user that creates the story
            entry (str): The text that the user entered as the entry of the story

        Throws:
            sqlite3.IntegrityError: title already exists

        Returns:
            None
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # replace " " with "_" because web url can't have space
    newtitle = title
    if " " in title:
        newtitle = title.replace(" ", "_")

    # add to story table, throws sqlite3.IntegrityError if title repeats.
    c.execute("INSERT INTO story VALUES(?,?,?)", (newtitle, user, entry))

    #save changes to database
    db.commit()

    # mark this story as being contributed by the user
    add_stories_contributed(newtitle, user)


def add_to_story(title, contributor, entry):
    """
    Add an entry and the contributor of that entry to story table

        Parameters:
            title (str): The title of the story that the user adds to
            contributor (str): The user that adds to the story
            entry (str): The text that the user entered as the entry of the story

        Returns:
            None
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # creates a dictionary to facilitate argument passing in the future
    dict = {"title":title, "contributor":contributor, "entry": entry}

    # get the contributor and entry from the current story
    command = "SELECT contributor, entry FROM story WHERE title=:title"
    # the field in dict would replace :title
    c.execute(command, dict)
    #stores the information as a list of tuples
    contributor_entry_list = c.fetchall()

    # add new information to contributor and entry through string concatenation, separated with \n
    entry_dict = contributor_entry_list[0][1] + "\n" + entry
    contributor_dict = contributor_entry_list[0][0] + "\n" + contributor

    # reset the dictionary to contain the most recent information
    dict['contributor'] = contributor_dict
    dict['entry'] = entry_dict

    #updates the database with the new dictionary
    c.execute("UPDATE story SET contributor = :contributor WHERE title =:title", dict)
    c.execute("UPDATE story SET entry = :entry WHERE title =:title", dict)
    db.commit()

    #mark this story as being contributed by the user
    add_stories_contributed(title, contributor)




def get_story_addable(username):
    """
    Returns titles of the stories that a user can add to

        Parameters:
            username (str): The user that the function is checking for

        Returns:
            addable_stories ([title1 (str), title2 (str), ... ]), the titles of the stories that the user has not contributed to
    """
    # avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # titles of all stories, each title in a tuple
    c.execute("SELECT title FROM story")
    titles = c.fetchall()

    # gets the stories contributed by the user
    stories_contributed = get_stories_contributed(username)

    addable_stories = []

    # add stories not contributed by the user to addable_stories
    for i in titles:
        if ((i[0] in stories_contributed) == False):
            addable_stories.append(i[0])

    return addable_stories


def get_story (title):
    """
    Returns all entries and users contributed to those entries of a story
        Parameters:
            title (str): title of the story

        Returns:
            story_list ([title (str), [contributor1 (str), contributor2 (str), ... ], [entry1 (str), entry2 (str), ...]]):
                the title, list of contributors, and list of entries to a story

    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #selects contributors and entry
    c.execute("SELECT contributor, entry FROM story WHERE title = :title", {"title":title})

    #[(contributor str, entries str)]
    entry_list = c.fetchall()
    story_list = [title]

    # add contributors and entries to story list
    for i in range(2):
        #split on each \n
        if(entry_list != []):
            story_list.append(entry_list[0][i].split('\n'))

    return story_list


def get_story_last_entry (title):
    """
    Returns the last entry for a story and the user contributed to that entry

        Parameters:
            title (str): title of the story

        Returns:
            last_entry_list ([contributor (str), last_entry (str)]):
                the user contributed to the last entry and the last entry
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use get_story to get the entire story
    last_entry_list = []
    big_list = get_story(title)

    # get last entry
    for i in range(2):
        # only want the contributor and entry but not the title
        last_entry_list.append(big_list[i+1][-1])

    return last_entry_list

def add_stories_contributed(title, contributor):
    """
    Adds a story to a user's stories_contributed column in the user_info table

        Parameters:
            title (str): title of the story that the user adds to
            contributor (str): the user that adds to the story

        Returns:
            None
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get the stories that the user has contributed
    c.execute("SELECT stories_contributed FROM user_info WHERE username =:contributor", {"contributor": contributor})
    a = c.fetchall()

    # append this story to the list
    if(a[0][0] != ""):
        stories_contributed = a[0][0] + "\n" + title
    else:
        stories_contributed = title

    #update the database
    dict = {"stories_contributed":stories_contributed, "contributor":contributor}
    c.execute("UPDATE user_info SET stories_contributed =:stories_contributed WHERE username = :contributor", dict)

    db.commit()

def get_stories_contributed(username):
    """
    Return the titles of the stories that the user contributed to

        Parameters:
            username (str): the user that we are getting

        Returns:
            stories_contributed ([title1 (str), title2 (str), ...]):
                the titles of the stories that the user contributed to
    """
    #avoid thread error
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # gets the stories that the user contributed to
    c.execute("SELECT stories_contributed FROM user_info WHERE username =:username", {"username": username})
    stories_contributed = c.fetchall()[0][0].split("\n")
    
    return stories_contributed
