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
    if(request.method == "POST"):
        if(request.form["type"] == "create"):
            db.create_story(request.form['title'], session["login"],request.form['content'])
        else:
            db.add_to_story(request.form["title"], session["login"],request.form["entry"])

    return render_template('home.html') # render login page with an error message

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

"""
to see how the add story functions work:
    uncomment  -- testing for add story -- part in db file, should just have the three manually add story
    c.execute statement and db.commit

    create account & login

    type in the search bar /add instead of /home, you should see some number of story2 or story3 (because
    story1 is marked as contributed manually in the get_addable_story function for testing)

    click on any of them, you should see last entries at the top and type in the input text section, click submitting

    you should be redirected to the add page once you click submit.

    click on the same story again, the last entry should show up as what you just entered
"""

#stories got added is weird because of the number of times the scripts in db file is called,
# should be fixed when everything is linked together and when i don't test with manual insert intos.
@app.route("/add", methods=['GET', 'POST'])
def add_story_list():

    #when you login the site, session["login"] would store which use is using
    story_list = db.get_story_addable(session["login"])

        #terminal testing prints
        #print("added to story")
        #print(get_story_last_entry(request.form["title"]))
    return render_template("add.html", collection = story_list)

#after submitting would go to the add page
@app.route("/add/<story>")
def add_a_story(story):
    #displays the contributor and the last entry of story
    last_entry = db.get_story_last_entry(story)
    return render_template("add_story.html",last_contributor=last_entry[0],last_entry = last_entry[1], title = story)

@app.route("/create", methods=['GET', 'POST'])
def create_story():
    return render_template("create.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    #db.db.close()
