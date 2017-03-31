from flask import Flask, render_template, flash,request,url_for,redirect,session
from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc




app = Flask(__name__)
app.secret_key = "sdkjgly"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/')
def homepage():
    if (session.get('logged_in') == True):
        if (session['logged_in'] == True):
            return redirect(url_for("history_page"))
        else:
            return redirect(url_for("login_page"))
    else:
        return redirect(url_for("login_page"))


@app.route('/forgot-password/')
def forgot_pass_page():
	return render_template("forgot-password.html")

@app.route('/photos/')
def photos_page():
	return render_template("photos.html")

@app.route('/home/<variable>')
@login_required
def dashboard(variable):
    if variable == session['username']:
        return render_template("home.html")
    else:
        return redirect(url_for("history_page"))
        #render_template("404.html")

@app.route('/upload/')
@login_required
def upload():
	flash("flash test!!!!")
	# flash("fladfasdfsaassh test!!!!")
	# flash("asdfas asfsafs!!!!")
	return render_template("upload.html")

@app.route('/database/')
def database():
    c, conn = connection()
    data = c.execute("SELECT * FROM Outward WHERE user_id = (%s)",[session['userid']])
    return render_template("database.html")

@app.route('/history/')
def history_page():
	flash("flash test!!!!")
	# flash("fladfasdfsaassh test!!!!")
	# flash("asdfas asfsafs!!!!")
	return render_template("history.html")

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
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])


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

            x = c.execute("SELECT * FROM User WHERE username = (%s)",[thwart(username)])

            if int(x) > 0:
                print ("That username is already taken, please choose another")
                print "int(x)>0"
                return render_template('sign-up.html', form=form, condition="Username already exists")

            else:
                data = c.execute("INSERT INTO User (username, password, email_id, department) VALUES (%s,%s,%s,%s)",
                	[ thwart(username), thwart(password), thwart(email), thwart('CSIT')])
                conn.commit()
                flash("Thanks for registering!")
                print "Thanks for registering"
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['userid'] = data
                session['username'] = username
                session['email'] = email
                return redirect(url_for('upload'))
        print "Nothing happened"
        return render_template("sign-up.html", form=form , conditon = "Please try again" )
    except Exception as e:
        print str(e)
        return(str(e))


@app.route('/login/', methods=["GET","POST"])
def login_page():
    if session.get('logged_in'):
        if session['logged_in']:
            return redirect(url_for("home"))
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM User WHERE username = (%s)",
                             [thwart(request.form['username'])])

            data = c.fetchone()
            password = data[1]
            email = data[2]
            userid = data[0]

            if sha256_crypt.verify(request.form['password'], password):
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['email'] = email
                session['userid'] = userid
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
