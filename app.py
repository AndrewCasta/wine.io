import os
from cs50 import SQL
from datetime import datetime
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
# app.config["SESSION_FILE_DIR"] = mkdtemp() # prevents session data staying on server
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
            error = 'Please enter username & password'

        # search DB for user_id
        user = db.execute("SELECT id, username, hash FROM users WHERE username = ?", username)
        # check username returns ONE results (if none, username doesn't exist)
        # check password HASH is same as db hash
        if len(user) != 1 or not check_password_hash(user[0]['hash'], password):
            error = 'Username or password incorrect'
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
    return render_template('login.html', error='Successfully logged out')

#################
# Frontend routes
#################

# ----
# Index (home)
# ----
@app.route("/")
@login_required
def index():

    # total reviews
    # SELECT count(*) from reviews WHERE user_id = 1
    totalReviews = db.execute('SELECT count(*) from reviews WHERE user_id = ?', session["user_id"])
    totalReviews = totalReviews[0]['count(*)']
    # drink again count
    # SELECT count(*) from reviews WHERE user_id = 1 AND drink_again = 'True'
    drinkAgainCount = db.execute("SELECT count(*) from reviews WHERE user_id = ? AND drink_again = 'True'", session["user_id"])
    drinkAgainCount = drinkAgainCount[0]['count(*)']

    # Recent 5 star rating
    # SELECT *, wines.* from reviews JOIN wines ON wine_id=wines.id WHERE user_id = 1 AND rating = 5 ORDER BY datetime DESC LIMIT 1
    recentTopRating = db.execute('SELECT *, wines.* from reviews JOIN wines ON wine_id=wines.id WHERE user_id = ? AND rating = 5 ORDER BY datetime DESC LIMIT 1', session["user_id"])
    if (len(recentTopRating) > 0):
        recentTopRating = recentTopRating[0]
    else:
        recentTopRating = None

    # most logged wine
    # SELECT wine_id, wines.brand, wines.variety, wines.year, COUNT(*) from reviews JOIN wines ON wine_id=wines.id WHERE user_id = 1 GROUP BY wine_id ORDER BY COUNT(*) DESC LIMIT 1
    mostReviewedWine = db.execute('SELECT wine_id, image, wines.brand, wines.variety, wines.year, COUNT(wine_id) from reviews JOIN wines ON wine_id=wines.id WHERE user_id = ? GROUP BY wine_id ORDER BY COUNT(*) DESC LIMIT 1', session["user_id"])
    if (len(mostReviewedWine) > 0):
        mostReviewedWine = mostReviewedWine[0]
    else:
        mostReviewedWine = None

    return render_template('index.html', user_id=session["user_id"], totalReviews=totalReviews, drinkAgainCount=drinkAgainCount, recentTopRating=recentTopRating, mostReviewedWine=mostReviewedWine)

# ----
# Add
# ----

# add new review

# set allowed file names
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template('add.html')

    # add wine to the DB
    if request.method == "POST":
        # collect all form data
        brand = request.form.get("brand")
        variety = request.form.get("variety")
        year = request.form.get("year")
        rating = request.form.get("rating")
        review = request.form.get("review")
        drink_again = request.form.get("drink_again")
        wine_id = request.form.get("wine_id")
        
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

        return redirect(url_for('reviews'))


# -------
# reviews
# -------

@app.route("/reviews")
@login_required
def reviews():
    return render_template('reviews.html')

# ----
# Edit
# ----

@app.route('/edit', methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "GET":
        error = None
        review_id = request.args.get('review_id')
        # search for review_id in DB with user_id
        review = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? AND reviews.review_id = ?", session['user_id'], int(review_id))
        
        # if none, error you don't have permission to edit that review
        if (len(review) == 0):
            error = 'Review not found for this user'
            return render_template('error.html', error=error)

        # if success, return edit page with review loaded
        return render_template('edit.html', review=review)

    # edit review end point
    if request.method == "POST":

        # get form details
        review_id = request.form.get("review_id")
        brand = request.form.get("brand")
        variety = request.form.get("variety")
        year = request.form.get("year")
        rating = request.form.get("rating")
        review = request.form.get("review")
        drink_again = request.form.get("drink_again")
        wine_id = request.form.get("wine_id")

        # image

        # if an image was on the form when loaded for editing and not changed, original value assigned here
        # if an image was not provided, or removed from the interface, this will be None
        image = request.form.get("image")

        # if new image file provided, this will override the previous image 
        # store in server folder & set image as location in db         
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(image)

        # if wine does exist, first create new row for wine, return wine_id
        if not wine_id:
            wine_id = db.execute("INSERT INTO wines (brand, variety, year) VALUES (?, ?, ?)", brand, variety, year)
        
        # then update DB row
        db.execute("UPDATE reviews SET wine_id = ?, rating = ?, review = ?, drink_again = ?, image = ? WHERE review_id = ? AND user_id = ?", wine_id, rating, review, drink_again, image, review_id, session["user_id"])

        # go back to review page
        return render_template('reviews.html')

# ------
# Delete
# ------
@app.route("/delete")
@login_required
def delete():
    # get review to be deleted
    review_id = request.args.get('review_id')

    db.execute("DELETE FROM reviews WHERE review_id = ? and user_id = ?", review_id, session["user_id"])

    return redirect(url_for('reviews'))


#############
# API routes
#############


@app.route('/api/')
def api():
    return render_template('api.html')

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
@login_required
def get_reviews():
    sortby = request.args.get("sort") # column name
    orderby = request.args.get("order") #ASC/DESC
    drink_again = request.args.get("drink_again")
    data = None

    # CS50 SQL doesn't support string variables as arguments (only numbers), so for the ASC/DESC or ORDER BY OPTIONAL values I've had to hard code SQL lookups.
    # Can't wait to learn a fuller SQL library!
    if drink_again:
        if sortby == 'rating' and orderby == 'DESC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? AND drink_again = 'True' ORDER BY rating DESC", session['user_id'])
        if sortby == 'rating' and orderby == 'ASC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? AND drink_again = 'True' ORDER BY rating ASC", session['user_id'])
        if sortby == 'datetime' and orderby == 'DESC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? AND drink_again = 'True' ORDER BY datetime DESC", session['user_id'])
        if sortby == 'datetime' and orderby == 'ASC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? AND drink_again = 'True' ORDER BY datetime ASC", session['user_id'])
    else:
        if sortby == 'rating' and orderby == 'DESC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? ORDER BY rating DESC", session['user_id'])
        if sortby == 'rating' and orderby == 'ASC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? ORDER BY rating ASC", session['user_id'])
        if sortby == 'datetime' and orderby == 'DESC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? ORDER BY datetime DESC", session['user_id'])
        if sortby == 'datetime' and orderby == 'ASC':
            data = db.execute("SELECT * FROM reviews JOIN wines ON reviews.wine_id=wines.id WHERE user_id = ? ORDER BY datetime ASC", session['user_id'])

    return jsonify(data)