import os
from cs50 import SQL
from flask import g, Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from functools import wraps
from pprint import pprint
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# set DB. Using SQL library from CS50.
db = SQL("sqlite:///wineio.db")

# File upload config
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
UPLOAD_FOLDER = 'static/images-upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Prevents JS cache issue - browser will not cache static assets that are served by Flask
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp() # prevents session data staying on server
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# TODO
# validate /add form data
# apply the login_require decorator to routes


#################
# Authentication
#################

# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# --------
# Register
# --------

@app.route('/register', methods=["GET", "POST"])
def register():
    #server register page
    if request.method == "GET":
        return render_template('register.html')

    # process user registration
    if request.method == "POST":
        error = None
        # get username and passwords from form
        username = request.form.get("username")
        password = request.form.get("password")
        password_check = request.form.get("password-check")

        # validate inputs
        # are not blank
        if not username or not password or not password_check:
            error = 'please enter all fields'
        # check passwords match
        if password != password_check:
            error = 'passwords did not match'

        # check username doesn't exist in db
        userCheck = db.execute('SELECT * FROM users WHERE username = ?', username)
        if len(userCheck) > 0:
            error = 'username already taken'

        # else register all good, proceed
        else:
            # insert new user into db (store username & password hash)        
            user_id = db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', username, generate_password_hash(password))
            # log user in
            session["user_id"] = user_id
            # redirect to index
            return redirect(url_for('index'))

        # redirect with error if failed
        return render_template('register.html', error=error)

# --------
# Login
# --------

@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # serve login page
    if request.method == "GET":
        return render_template('login.html')

    # process login & redirect to index
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        # validate inputs
        # username & password inputted
        if not username or not password:
            error = 'please enter username & password'

        # search DB for user_id
        user = db.execute("SELECT id, username, hash FROM users WHERE username = ?", username)
        # check username returns ONE results (if none, username doesn't exist)
        # check password HASH is same as db hash
        if len(user) != 1 or not check_password_hash(user[0]['hash'], password):
            error = 'username or password incorrect'
        # store user_id as session["user_id"] & redirect
        else:
            session["user_id"] = user[0]['id']
            return redirect(url_for('index'))
        
        # if not match, return error message
        return render_template('login.html', error=error)

# --------
# Logout
# --------

@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()
    # redirect to login
    return url_for('index')

#################
# Frontend routes
#################

# ----
# Index (home)
# ----
@app.route("/")
@login_required
def index():
    return render_template('index.html', user_id=session["user_id"])

# ----
# Add
# ----

# add new review
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    if request.method == "POST":
        session["user_id"] = 1 # ===========================================================<<<< TODO
        # collect all form data
        brand = request.form.get("brand")
        variety = request.form.get("variety")
        year = request.form.get("year")
        rating = request.form.get("rating")
        review = request.form.get("review")
        drink_again = request.form.get("drink_again")
        wine_id = request.form.get("wine_id")
        # needs to implement autocomplete, then check for wine_id if a match was found 

        # validate all form data ===========================================================<<<< TODO
        
        # image
        # if image file provided, store in server folder & set image as location in db
        file = request.files['file']
        image = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(image)
        # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

        # update all form data in db
        # if wine does exist, first create new row for wine, return wine_id
        if not wine_id:
            wine_id = db.execute("INSERT INTO wines (brand, variety, year) VALUES (?, ?, ?)", brand, variety, year)
        # insert review into DB
        db.execute("INSERT INTO reviews (user_id, wine_id, rating, image, review, drink_again) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], wine_id, rating, image, review, drink_again)

        return redirect(url_for('add'))


# -------
# reviews
# -------

@app.route("/reviews")
def reviews():
    session["user_id"] = 1 # ===========================================================<<<< TODO
    return render_template('reviews.html')


# ------
# Detail
# ------

# ----
# Edit
# ----

#############
# API routes
#############


@app.route('/api/')
def api():
    return

# -----
# Wines
# -----

# wines lookup (return wines to frontend for lookup & return to DB via add route)
@app.route('/api/wines')
def get_wines():
    data = {}
    data["wines"] = db.execute("SELECT * FROM wines")
    return data

# -----------
# review data
# -----------

@app.route("/api/reviews")
def get_reviews():
    session['user_id'] = 1 # ===========================================================<<<< TODO

    sortby = request.args.get("sort") # column name
    orderby = request.args.get("order") #ASC/DESC
    drink_again = request.args.get("drink_again")

    # Can't figure out succinct way to pass OPTIONAL values to the SQL string using the CS50 SQL library so I've create multiple SELECTs at this route depending on the args :(
    if drink_again:
        data = db.execute("SELECT * FROM reviews WHERE user_id = ? AND drink_again = ? ORDER BY ?", session['user_id'], drink_again, sortby)
    else:
        data = db.execute("SELECT * FROM reviews WHERE user_id = ? ORDER BY ?", session['user_id'], sortby)

    # Return
    # Join reviews AND wines from db

    return jsonify(data)