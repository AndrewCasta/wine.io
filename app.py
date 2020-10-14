import os
from cs50 import SQL
from flask import g, Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from functools import wraps
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
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# hardcoded user


# TODO
# validate /add form data
# check wine_id from front end works


#################
# Authentication
#################

# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#################
# Frontend routes
#################


@app.route("/")
def index():
    session["user_id"] = 1
    return render_template('index.html', user_id=session["user_id"])

# add new review
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    if request.method == "POST":
        # hack user 1 for testing
        session["user_id"] = 1
        # collect all form data
        brand = request.form.get("brand")
        variety = request.form.get("variety")
        year = request.form.get("year")
        rating = request.form.get("rating")
        review = request.form.get("review")
        drink_again = request.form.get("drink_again")
        wine_id = request.form.get("wine_id")
        # needs to implement autocomplete, then check for wine_id if a match was found 

        # TODO validate all form data
        
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

#############
# API routes
#############

# wines lookup (return wines to frontend for lookup & return to DB via add route)
@app.route('/wines')
def get_wines():
    data = {}
    data["wines"] = db.execute("SELECT * FROM wines")
    return data

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

# review lookup (for editing)


