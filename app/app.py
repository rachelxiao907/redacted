from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #allow for session creation/maintenance
from flask import redirect
from os import urandom
import db
import sqlite3   #enable control of an sqlite database

app = Flask(__name__)    #create Flask object
app.secret_key = urandom(32) #generates random key

"""
To see how everything works (Yuqing just tested for one user so)
    Create account & login

    Click create a story, enter fields.

    You should be redirected to home page, click add to story

    you should see the story you created, click on it

    you should see your username and entry you last entered when creating it. Enter a new entry.

    You should be redirected to home page, click add to story again, you shouldn't see anything since you can't
    add to a story twice

Somebody test out multi users.
"""
@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    # print("***DIAG: request.args ***")
    # print(request.args)
    # print("***DIAG: request.args['username']  ***")
    # print(request.args['username']) -- does NOT work - this has not been defined yet - causes error
    print("***DIAG: request.headers ***")
    print(request.headers)

    # checks for request method and gets the input
    data = []
    if(request.method == "GET"):
        data = request.args
    else:
        data = request.form
    if("sub2" in data): # sub2 is added to request.args when the user has logged out, so we can check if it exists to determine whether to end the session or not
        session["login"] = False # end session
    if("login" in session):
        if(session["login"] != False): # if not false, the value of session["login"] is the username of the logged in user
            return redirect("/home") # go straight to home page
    print(session)
    if("username" in data):
        # checks for request method and gets the input
        if(request.method == "GET"):
            name_input = request.args['username']
            pass_input = request.args['password']
        else:
            name_input = request.form['username']
            pass_input = request.form['password']


        error = "" # the error message
        # a try catch block in case anything unexpected happens
        try:
            error = db.get_login(name_input, pass_input)
            if(error == ""):
                session["login"] = name_input
                print("hello")
                return redirect("/home") # render welcome page
        except Exception as e:
            error = e
        return render_template('login.html', error_message = error) # render login page with an error message
    return render_template('login.html') # otherwise render login page


@app.route("/home", methods=['GET', 'POST'])
def load_home():
    if("login" in session and not(session["login"] == False)):
        if(request.method == "POST"):
            db.add_to_story(request.form["title"], session["login"],request.form["entry"])
        past_stories = db.get_stories_contributed(session["login"])
        list_story = []
        for i in past_stories:
            list_story.append(db.get_story(i))

        return render_template('home.html', name = session["login"], story_col = list_story) # render login page with an error message
    else:
        return redirect("/")


@app.route("/create_account", methods=['GET', 'POST'])
def create_account_render():
    # check if input exists by checking if username input is in request dictionary
    if('username' in request.form or 'username' in request.args):
        name_input = "" #username input
        pass_input = "" #password input
        cpass_input = "" #confirm password
        error = "" # error message
        # checks for request method and gets the input
        if(request.method == "GET"):
            name_input = request.args['username']
            pass_input = request.args['password']
            cpass_input = request.args['cpassword']
        else:
            name_input = request.form['username']
            pass_input = request.form['password']
            cpass_input = request.form['cpassword']
        # checks input for validity (it exists, passwords match, etc.)
        if(name_input == ""):
            error = "Username field cannot be blank!"
        elif(pass_input == ""):
            error = "Password field cannot be blank!"
        elif("\\n" in name_input):
            error = "Username cannot contain \\n!"
        elif(pass_input != cpass_input):
            error = "Password fields must match!"
        else:
            try:
                db.add_login(name_input, pass_input) # try to add u/p pair to db
                return redirect("/") # go back to main login page
            except sqlite3.IntegrityError: # will throw this error if the username is a duplicate
                error = "Username already exists!"
        # render the page after processing input
        return render_template('create_account.html', error_message=error)
    # render the page
    return render_template('create_account.html')


#stories got added is weird because of the number of times the scripts in db file is called,
# should be fixed when everything is linked together and when i don't test with manual insert intos.
@app.route("/add", methods=['GET', 'POST'])
def add_story_list():
    if("login" in session and not(session["login"] == False)):
    #when you login the site, session["login"] would store which use is using
        story_list = db.get_story_addable(session["login"])

            #terminal testing prints
            #print("added to story")
            #print(get_story_last_entry(request.form["title"]))
        return render_template("add.html", collection = story_list)
    else:
        return redirect("/")


#after submitting would go to the add page
@app.route("/add/<story>")
def add_a_story(story):
    if("login" in session and not(session["login"] == False)):
        #displays the contributor and the last entry of story
        last_entry = db.get_story_last_entry(story)
        title = ""
        for i in story:
            if i == " " or i == "\\":
                title+="_"
            else:
                title += i

        return render_template("add_story.html", last_contributor=last_entry[0],last_entry = last_entry[1], title = title)
    else:
        return redirect("/")


@app.route("/create", methods=['GET', 'POST'])
def create_story():
    if("login" in session and not(session["login"] == False)):
        if(request.method == "POST"):
            print(request.form)
            try:
                db.create_story(request.form['title'], session["login"],request.form['content'])
                return redirect("/home")
            except sqlite3.IntegrityError:
                return render_template('create.html', message = "Title already exists" )
        else:
            return render_template("create.html", message = "")
    else:
        return redirect("/")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    db.db.close()
