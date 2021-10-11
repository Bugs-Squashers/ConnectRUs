from flask import Flask, session, redirect
import pymongo

# Create a flask app
app = Flask(__name__)
app.secret_key = "supersecretekey"

# # setting up a local db
client = pymongo.MongoClient("localhost", 27017)
# set the db to the connectrus database. creates one if there isn't one
db = client.connectrus

# # the db connected to the cloud
# client = pymongo.MongoClient("mongodb+srv://Amanda:<HEi5PECVhPbG6ZOk>@connectrus.ydbwi.mongodb.net/connectrus?retryWrites=true&w=majority")
# db = client.test

# set variable to collection called users. creates one if there isn't one
users = db.users


# Sessions is used to keep the user logged in until they logged out
# it also stores the username so we can easily grab info for that user from the db

# Home page
@app.route('/')
def hello():
    if 'username' in session:
        userData = users.find_one({'username': session['username']})
        return "Hello " + userData['name'] + "!"
    return "Hello World!"


# signup
# TODO: make sure no inputs are null, and no illegal characters
@app.route('/signup/<username>/<password>/<name>')
def signup(username, password, name):
    # if the count matches the limit it returns true, else false
    if users.count_documents({'username': username}, limit=1):
        return "username already exists!"
    else:
        # username is unique so we add the user to the db
        data = {'username': username, 'password': password, 'name': name, 'groups': []}
        users.insert_one(data)
        session.permanent = True
        session['username'] = username
        return redirect('/')


# TODO: if a user is already logged in the page should block them from inputting login info
@app.route('/login/<username>/<password>')
def login(username, password):
    # if the username exists in the db
    if users.count_documents({'username': username}, limit=1):
        # check that the password is correct
        userData = users.find_one({'username': username})
        if userData['password'] == password:
            session.permanent = True
            # set the session's username to the username that just logged in
            session['username'] = username
            return redirect('/')
        else:
            return "Wrong Password!"
    else:
        # TODO: this should be a pop up or something, so user can still attempt to login
        return "That username already exists! Or someone is logged in already"


# logout
@app.route('/logout')
def logout():
    # remove the username from the session, now there are no users logged into the session
    session.pop('username', None)
    return redirect('/')

# shows groups that the user is part of
@app.route('/groups')
def groups():
    # check if there is a user logged in
    if 'username' in session:
        # pull up the data for the logged in user
        userData = users.find_one({'username': session['username']})
        output = userData['name'] + "'s Groups: "
        # if the user is not in any groups
        if len(userData['groups']) == 0:
            return output + "You aren't in any groups!"
        return output + str(userData['groups'])
    return "Please login to view groups"

# create a group
@app.route('/createGroup/<groupid>')
def createGroup(groupid):
    # check that there is a user logged in
    if 'username' in session:
        if db.groups.count_documents({'groupid': groupid}, limit=1):
            return "This group ID already exists! Please make a different one."
        else:
            data = {'groupid': groupid, 'members': session['username']}
            db.groups.insert_one(data)
            # add the groupid to the user's data
            users.update_one({'username': session['username']}, {'$push': {'groups': groupid}})
            return redirect('/groups')
    return "Please login to create groups"


# delete a group
#TODO: doesn't delete from user's 'group' list but it does delete from the group db
@app.route('/deleteGroup/<groupid>')
def deleteGroup(groupid):
    # check that there is a user logged in
    if 'username' in session:
        if db.groups.count_documents({'groupid': groupid}, limit=1):
            db.groups.delete_one({'groupid': groupid})
            # also need to delete the group from any user's data
            for user in users.find({"group": groupid}):
                db.user.update({'_id': user['_id']}, {'$pull': {"group": groupid}})
            return redirect('/groups')
        else:
            return "this group ID doesn't exist!"
    return "Please login to create groups"


app.run(host="0.0.0.0")
