# Team F^2: Michael Borczuk, Yuqing Wu, David Chong
# SoftDev
# K15 -- Sessions Greetings
# 2021-10-19

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #allow for session creation/maintenance
from os import urandom
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = urandom(32) #generates random key
@app.route("/") #, methods=['GET', 'POST'])
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
            return render_template('response.html', name=session["login"], req=request.method) # if session still exists go straight to login page
    print(session)
    return render_template( 'login.html') # otherwise render login page


@app.route("/auth") # , methods=['GET', 'POST'])
def authenticate():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.args)
    #print("***DIAG: request.args['username']  ***")
    #print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)


    #should work but I don't know how to change the request type so it's not thoroughly tested
    name_input = "" #username input
    pass_input = "" #password input
    
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
        #check to see if the login is correct first, because the login should default to incorrect
        if(name_input == "fsquared" and pass_input == "isthebest"):
            session["login"] = name_input # set session to the username
            print(session)
            return render_template('response.html', name=name_input, req=request.method) # render welcome page

        if(name_input != "fsquared"): # username is wrong
            error = "Error, User Not Found"
        elif(pass_input != "isthebest"): #password is wrong
            error = "Error, Username and Password Do Not Match"
        else:
            error = "Error"
    except:
        error = "Error"
    return render_template( 'login.html', error_message = error) # render login page with an error message




if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
