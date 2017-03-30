from flask import Flask, render_template, flash,request,url_for,redirect,session
from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc

from content_management import Content
TOPIC_DICT = Content()


app = Flask(__name__)
app.secret_key = "sdkjgly"


@app.route('/')
def homepage():
	return render_template("history.html")


@app.route('/forgot-password/')
def forgot_pass_page():
	return render_template("forgot-password.html")

@app.route('/dashboard/')
def dashboard():
	flash("flash test!!!!")
	# flash("fladfasdfsaassh test!!!!")
	# flash("asdfas asfsafs!!!!")
	return render_template("home.html")

@app.route('/upload/')
def upload():
	flash("flash test!!!!")
	# flash("fladfasdfsaassh test!!!!")
	# flash("asdfas asfsafs!!!!")
	return render_template("upload.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])


@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        print "inside register page"
        if request.method == "POST" :
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",[thwart(username)])
            
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                print "int(x)>0"
                return render_template('sign-up.html', form=form, condition="Username already exists")

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s,%s,%s,%s)", 
                	[ thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")])
                conn.commit()
                flash("Thanks for registering!")
                print "Thanks for registering"
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('upload'))
        print "Nothing happened"
        return render_template("sign-up.html", form=form , conditon = "Please try again" )

    except Exception as e:
        print str(e)
        return(str(e))


@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             [thwart(request.form['username'])])
            
            data = c.fetchone()[2]


            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                print session['username']
                print ("You are now logged in")
                return redirect(url_for("upload"))

            else:
                error = "Invalid credentials, try again."
                print error

        gc.collect()
        
        return render_template("sign-in.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        print error
        return render_template("sign-in.html", error = error)  
		

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    #flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('upload'))

if __name__ =="__main__":
	app.debug = True
	app.run()
