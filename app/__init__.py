from flask import Flask, render_template, request, session, redirect
from os import urandom
import db
import sqlite3   #enable control of an sqlite database

app = Flask(__name__) #create Flask object
app.secret_key = urandom(32) #generates random key

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    data = [] #
    # check request method to use the right method for accessing inputs
    if (request.method == 'GET'):
        data = request.args
    else:
        data = request.form
    #print(data) #ImmutableMultiDict([('username', 'a'), ('password', 'a'), ('sub1', 'Login')])

    if ('sub2' in data): # sub2 is the logout button. user clicking it puts sub2 into data and ends the session
        session['login'] = False # end session
    if ('login' in session): # login is the login button
        if (session['login'] != False): # if user is not logged out, session['login'] is the user's username
            return redirect("/home") # landing page after login
    #print(session)

    if ('username' in data):
        if(request.method == 'GET'):
            name_input = request.args['username']
            pass_input = request.args['password']
        else:
            name_input = request.form['username']
            pass_input = request.form['password']

        error = "" # error message
        # a try catch block for anything unexpected happening
        try:
            error = db.get_login(name_input, pass_input) # check if the user exists in database
            if(error == ""):
                session["login"] = name_input # session username is stored
                print("hello") #check is the username was stores
                return redirect("/home") # render welcome page
        except Exception as e:
            error = e
        return render_template('login.html', error_message = error) # render login page with the correct error message
    return render_template('login.html') # otherwise render login page

@app.route("/home", methods=['GET', 'POST'])
def load_home():
    if('login' in session and not(session['login'] == False)):
        if(request.method == 'POST'): # input from add/<story> page
            db.add_to_story(request.form['title'], session['login'], request.form['entry'])
        past_stories = db.get_stories_contributed(session['login'])
        list_story = []
        for i in past_stories:
            list_story.append(db.get_story(i))
        return render_template('home.html', name = session['login'], story_col = list_story) # render home page with username
    else:
        return redirect("/")


@app.route("/create_account", methods=['GET', 'POST'])
def create_account_render():
    if('username' in request.form or 'username' in request.args): # check if input exists by checking if username input is in request dictionary
        name_input = "" #username input
        pass_input = "" #password input
        cpass_input = "" #confirm password
        error = "" # error message
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
            except sqlite3.IntegrityError: # error if the username is a duplicate
                error = "Username already exists!"
        return render_template('create_account.html', error_message = error)
    return render_template('create_account.html')


# stories got added is weird because of the number of times the scripts in db file is called
# should be fixed when everything is linked together and with better testing
@app.route("/add", methods=['GET', 'POST'])
def add_story_list():
    if('login' in session and not(session['login'] == False)):
        story_list = db.get_story_addable(session['login']) # stories the user can add to
        #print("added to story")
        #print(get_story_last_entry(request.form["title"]))
        return render_template("add.html", collection = story_list)
    else:
        return redirect("/")

# after submitting would go to the add page
@app.route("/add/<story>")
def add_a_story(story): # story is the title of the story
    if('login' in session and not(session['login'] == False)):
        last_entry = db.get_story_last_entry(story) # displays the contributor and the last entry of story
        title = ""
        for i in story: # makes url have _ replace the spaces
            if i == " " or i == "\\":
                title += "_"
            else:
                title += i
        return render_template("add_story.html", last_contributor = last_entry[0], last_entry = last_entry[1], title = story)
    else:
        return redirect("/")

@app.route("/create", methods=['GET', 'POST'])
def create_story():
    if('login' in session and not(session['login'] == False)):
        if(request.method == 'POST'):
            #print(request.form)
            if(not(request.form['title'] and request.form['title'].strip())):
                return render_template('create.html', message = "Please have a title")
            else:
                if(not(request.form['content'] and request.form['content'].strip())):
                    return render_template('create.html', message = "Please start the story")
            try:
                db.create_story(request.form['title'], session['login'],request.form['content'])
                return render_template('create.html', message = "You've created a story!")
            except sqlite3.IntegrityError: # title is a unique type in the datatable
                return render_template('create.html', message = "Title already exists")
        else:
            return render_template("create.html", message = "")
    else:
        return redirect("/")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    db.db.close()
