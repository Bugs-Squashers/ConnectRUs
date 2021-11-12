from flask import Flask, session, redirect, request, render_template
import pymongo
import datetime

# Create a flask app
app = Flask(__name__)
app.secret_key = "supersecretekey"

# connect to the hosted database
client = pymongo.MongoClient(
    "mongodb+srv://Amanda:HEi5PECVhPbG6ZOk@connectrus.ydbwi.mongodb.net/connectrus?retryWrites=true&w=majority")
# database name is test
db = client.test
# collection is named users
users = db.users
trial = db.trial


# # For local db
# client = pymongo.MongoClient("localhost", 27017)
# db = client.connectrus
# users = db.users
# trial = db.trial

#################NOTES#######################
# Sessions is used to keep the user logged in until they logged out
# it also stores the username so we can easily grab info for that user from the db
# if request.method == "POST" means the user has submitted the form by clicking the button

# Home page
@app.route('/')
def hello():
    if 'username' in session:
        userData = users.find_one({'username': session['username']})
        msg = "Hello " + userData['name'] + "!"
        return render_template("index.html", value=msg)
    return render_template("index.html")


# signup
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session.permanent = True
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        # check if input has blank or space
        if username == "" or (" " in username) or password == "" or (" " in password) or name == "":
            return render_template("message.html",
                                   value="Please enter a valid username and password. No spaces allowed.")
        # if the count matches the limit it returns true, else false
        if users.count_documents({'username': username}, limit=1):
            return render_template("message.html", value="username already exists!")
        else:
            data = {'username': username, 'password': password, 'name': name, 'groups': []}
            users.insert_one(data)
            session['username'] = username
            return redirect('/')
    else:
        if 'username' in session:
            return render_template("message.html", value="Already logged in")
        # if no one logged in, show the signup page
        return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form['username']
        password = request.form['password']
        # check if input has blank or space
        if username == "" or (" " in username) or password == "" or (" " in password):
            return render_template("message.html", value="Please enter a valid username and password")
        # if the username exists in the db
        if users.count_documents({'username': username}, limit=1):
            # check that the password is correct
            userData = users.find_one({'username': username})
            if userData['password'] == password:
                # set the session's username to the username that just logged in
                session['username'] = username
                return redirect('/')
            else:
                return render_template("message.html", value="Wrong Password!")
        else:
            return render_template("message.html", value="That username doesn't exist!")
    else:
        if 'username' in session:
            return render_template("message.html", value="Already logged in")
        # if no one logged in, show the login page
        return render_template("login.html")


# logout
@app.route('/logout')
def logout():
    # remove the username from the session, now there are no users logged into the session
    session.clear()
    return redirect('/')


# TODO: create unique event name, only allow 30 minute increments to be stored (maybe an html thing)
# TODO: make sure end > start
@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == "POST":
        # start = request.form.get('start')
        # # end = request.form.get['end']
        # string = start.strftime('%A')
        ##########################################################
        date = request.form.get('date')
        ##########################################################
        start = request.form.get('start')
        end = request.form.get('end')
        print(start)
        start_datetime = datetime.datetime.strptime(date + " " + start, "%Y-%m-%d %H:%M")
        end_datetime = datetime.datetime.strptime(date + " " + end, "%Y-%m-%d %H:%M")

        # TODO: make sure no duplicates for same event (aka event name should be unique)
        # TODO: in html (?) plz let user only choose 30 min interval times
        delta = datetime.timedelta(minutes=30)
        data = {'eventname': 'test', 'date': date, start_datetime.strftime('%H:%M'): []}
        trial.insert_one(data)
        while start_datetime < end_datetime:
            start_datetime = start_datetime + delta
            trial.update_one({'eventname': 'test'}, {'$set': {start_datetime.strftime('%H:%M'): []}})

        result = start_datetime.strftime('%c') + ' ' + end_datetime.strftime('%c')
        return render_template("testing.html", value=result)
    return render_template("scheduling.html")


# TODO: can only add times that are within the event time
# TODO: search for correct event to add to
# TODO: don't allow repeats
@app.route('/available', methods=['GET', 'POST'])
def available():
    # if 'username' in session:
    if 'username' in session:
        userData = users.find_one({'username': session['username']})
        if request.method == "POST":
            # take the string of time from html
            from_string = request.form.get('available_from')
            to_string = request.form.get('available_to')
            # convert the string into datetime obj so we can increment it later
            available_from = datetime.datetime.strptime(from_string, '%H:%M')
            available_to = datetime.datetime.strptime(to_string, '%H:%M')

            delta = datetime.timedelta(minutes=30)

            while available_from <= available_to:
                trial.update_one({'eventname': 'test'}, {'$push': {available_from.strftime('%H:%M'): userData['name']}})
                available_from = available_from + delta
            return "Added Availability"
        else:
            return render_template("available.html")
    return "please login"


@app.route('/time', methods=['GET'])
def time():
    eventData = trial.find_one({'eventname': 'test'}, {"_id": 0, "eventname": 0, "date": 0})
    data = []
    for key in eventData:
        temp = []
        temp.append(key)
        for x in eventData.get(key):
            temp.append(x)
        data.append(temp)
    return render_template("time.html", data=data)


# commented these out because they need to be fixed/don't have a html yet

# # shows groups that the user is part of
# @app.route('/groups', methods=["GET"])
# def groups():
#     # check if there is a user logged in
#     if 'username' in session:
#         # pull up the data for the logged in user
#         userData = users.find_one({'username': session['username']})
#         output = userData['name'] + "'s Groups: "
#         # if the user is not in any groups
#         if len(userData['groups']) == 0:
#             return output + "You aren't in any groups!"
#         return output + str(userData['groups'])
#     return "Please login to view groups"
#
# # create a group
# @app.route('/createGroup/<groupid>')
# def createGroup(groupid):
#     # check that there is a user logged in
#     if 'username' in session:
#         if db.groups.count_documents({'groupid': groupid}, limit=1):
#             return "This group ID already exists! Please make a different one."
#         else:
#             data = {'groupid': groupid, 'members': session['username']}
#             db.groups.insert_one(data)
#             # add the groupid to the user's data
#             users.update_one({'username': session['username']}, {'$push': {'groups': groupid}})
#             return redirect('/groups')
#     return "Please login to create groups"
#
#
# # delete a group
# #TODO: doesn't delete from user's 'group' list but it does delete from the group db
# @app.route('/deleteGroup/<groupid>')
# def deleteGroup(groupid):
#     # check that there is a user logged in
#     if 'username' in session:
#         if db.groups.count_documents({'groupid': groupid}, limit=1):
#             db.groups.delete_one({'groupid': groupid})
#             # also need to delete the group from any user's data
#             for user in users.find({"group": groupid}):
#                 db.user.update({'_id': user['_id']}, {'$pull': {"group": groupid}})
#             return redirect('/groups')
#         else:
#             return "this group ID doesn't exist!"
#     return "Please login to create groups"


app.run(host="0.0.0.0")
