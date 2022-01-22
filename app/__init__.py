from flask import Flask, render_template, request, session, redirect
from os import urandom
import db
import sqlite3   #enable control of an sqlite database

app = Flask(__name__) #create Flask object
app.secret_key = urandom(32) #generates random key

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    '''
    Renders the login page where users can login or be redirected accordingly.
        Takes user inputs from the main page and checks the username/password against the database.
        Check if there is a session to redirect user to the landing page if user is logged in.
    '''
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
            return redirect(url_for('load_home')) # landing page after login
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
                #print("hello") #check is the username was stores
                return redirect(url_for('load_home')) # render landing page
        except Exception as e:
            error = e
        return render_template('login.html', error_message = error) # render login page with the correct error message
    return render_template('login.html') # otherwise render login page


@app.route("/home", methods=['GET', 'POST'])
def load_home():
    '''
    Renders landing page that displays all the stories the user has contributed to when they have logged in.
    Stores user inputs of adding to a story as the user is redirected to the landing page after submitting.
    '''
    if('login' in session and session['login'] != False): # user can only access the other pages if they are logged in
        if(request.method == 'POST'): # input from add/<story> page
            entry_list = request.form['entry'].split('\n')
            #print(entry_list)
            entry = ' '.join(entry_list) # replace new lines with spaces
            #print(entry)
            db.add_to_story(request.form['title'], session['login'], entry)
        past_stories = db.get_stories_contributed(session['login'])
        list_story = []
        for i in past_stories: # for ever title in the list of stories contributed
            list_story.append(db.get_story(i))
        return render_template('home.html', name = session['login'], story_col = list_story) # render home page with username
    else:
        return redirect(url_for('disp_loginpage'))


@app.route("/create_account", methods=['GET', 'POST'])
def create_account_render():
    '''
    Renders the page that holds a create account form.
        Creates account only if the username is unique in the database, if the user's passwords match,
        and if it passes the requirements.
    '''
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
                return redirect(url_for('disp_loginpage')) # go back to login page
            except sqlite3.IntegrityError: # error if the username is a duplicate
                error = "Username already exists!"
        return render_template('create_account.html', error_message = error)
    return render_template('create_account.html')


@app.route("/add", methods=['GET', 'POST'])
def add_story_list():
    '''
    Renders the add page which displays all the stories the user can contribute to.
    '''
    if('login' in session and session['login'] != False): # user can only access the other pages if they are logged in
        story_list = db.get_story_addable(session['login']) # stories the user can add to
        #print("added to story")
        #print(get_story_last_entry(request.form["title"]))
        return render_template("add.html", collection = story_list)
    else:
        return redirect(url_for('load_home'))


@app.route("/add/<story>")
def add_a_story(story): # story is the title of the story
    '''
    Renders the specific page for a story and displays the last entry and contributor on the page.
    '''
    if('login' in session and not(session['login'] == False)): # user can only access the other pages if they are logged in
        story_list = db.get_story_addable(session['login']) # displays the contributor and the last entry of story
        if(story in story_list):
            last_entry = db.get_story_last_entry(story)
            return render_template("add_story.html", last_contributor = last_entry[0], last_entry = last_entry[1], title = story)
    else:
        return redirect(url_for('load_home'))


@app.route("/create", methods=['GET', 'POST'])
def create_story():
    '''
    Takes inputs from the create story form and displays error messages depending on the user's title and story inputs.
        Checks if the title is unique and has slashes because the title will have a url.
    '''
    if('login' in session and session['login'] != False): # user can only access the other pages if they are logged in
        if(request.method == 'POST'):
            #print(request.form)
            if(not(request.form['title'] and request.form['title'].strip())): # if title is blank or only has spaces
                return render_template('create.html', message = "Please have a title")
            elif(not(request.form['content'] and request.form['content'].strip())): # if story is blank
                return render_template('create.html', message = "Please start the story")
            elif("/" in request.form['title'] or "\\" in request.form['title']): # slashes are special characters that affect the url
                return render_template('create.html', message = "Please omit slashes in the title")
            else:
                content_list = request.form['content'].split('\n')
                content = ' '.join(content_list)
            try:
                db.create_story(request.form['title'], session['login'], content)
                return render_template('create.html', message = "You've created a story!")
            except sqlite3.IntegrityError: # title is a unique type in the datatable
                return render_template('create.html', message = "Title already exists", story = content)
        else:
            return render_template("create.html", message = "")
    else:
        return redirect(url_for('load_home'))


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
    db.db.close()
