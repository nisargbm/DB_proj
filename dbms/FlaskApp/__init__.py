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

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    department = TextField('Department')
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])

@app.route('/')
def homepage():
	if(session.get('logged_in')):
		if(session['logged_in']):
			return redirect(url_for('home'))
	return render_template("homepage.html")


@app.route('/forgot-password/')
def forgot_pass_page():
	return render_template("forgot-password.html")

@app.route('/photos/')
def photos_page():
	return render_template("photos.html")

@app.route('/home')
@login_required
def home():
	c, conn = connection()
	#QUERY For Pending Documents
	c.execute("SELECT * FROM User")
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("home.html", data=data)

@app.route('/outward/')	
@login_required
def outward():
	#c,conn =connection()
	return render_template("outward_form.html")

@app.route('/upload/')
@login_required
def upload():
	flash("flash test!!!!")
	# flash("fladfasdfsaassh test!!!!")
	# flash("asdfas asfsafs!!!!")
	return render_template("upload.html")

@app.route('/existing_doc/<variable>')
@login_required
def existing_doc(variable):
    c, conn = connection()
    c.execute("SELECT * FROM User WHERE user_id = (%s)", [thwart(variable)])
    #conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("existing_doc.html", data = data)

@app.route('/my_docs/')
@login_required
def my_docs():
	c, conn = connection()
	c.execute("SELECT doc_id,subject,details FROM Process NATURAL JOIN Document_details WHERE user_id = 'om' AND status= 'CREATED' ORDER BY movement_date DESC;")
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("my_docs.html", data = data)


class InwardNewForm(Form):
	userid = TextField('user_id')
	subject = TextField('subject',[validators.Length(min = 1, max = 255)])
	doc_details = TextField('document_details')
	organization = TextField('organization',[validators.Length(min = 1, max = 1000)])
	no_docs = TextField('no_documents')
	to = TextField('forward_person')
	# place = TextField('place_of_recieving',[validators.Length(min = 1,max = 1000)]) 

@app.route('/new_doc/', methods=["GET","POST"])
@login_required
def new_doc():
	try:
		c, conn = connection()
		form = InwardNewForm(request.form)		
		if request.method == "POST" :
			sender  = form.userid.data
			subject = form.subject.data
			doc_details = form.doc_details.data
			org = form.organization.data
			no_docs = form.no_docs.data
			reciever = form.to.data
			# place = form.place.data
			print (sender)
			print (subject)
			print (doc_details)
			print (org)
			print (no_docs)
			print(reciever)
				# TODO : queries by hemang and maneesh

				# c.execute("INSERT INTO Document_details (subject, number_of_documents, organisation, details) VALUES (%s,%s,%s,%s)",
				# 	[ thwart(subject), thwart(no_docs), thwart(org), thwart(doc_details)])
				# conn.commit()

				# c.execute("INSERT INTO Document(reciever,sender, organisation, details) VALUES (%s,%s,%s,%s)",
				# 	[ thwart(subject), thwart(no_docs), thwart(org), thwart(doc_details)])
				# conn.commit()

				# c.execute("INSERT INTO Document(reciever,sender, organisation, details) VALUES (%s,%s,%s,%s)",
				# 	[ thwart(subject), thwart(no_docs), thwart(org), thwart(doc_details)])
				# conn.commit()
			print("Thanks for uploading!")
			c.close()
			conn.close()
			gc.collect()
			return redirect(url_for('home'))
		else:
			c.execute("SELECT DISTINCT department FROM User")
			conn.commit()
			data = c.fetchall()
			dept = []
			for u in data:
				dept.append(u[0])
			users = []
			for d in dept:
				c.execute("SELECT user_id FROM User WHERE department = (%s)",[thwart(d)])
				conn.commit()
				data = c.fetchall()
				names = []
				for u in data:
					names.append(u[0])
				users.append(names)
			return render_template("new_doc.html",form=form, users = users, dept = dept)
	except Exception as e:
		print (str(e))
		return(str(e))

@app.route('/database/')
def database():
    c, conn = connection()
    c.execute("SELECT * FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("database.html", data = data)

@app.route('/history/received')
def history_recieved():
	c, conn = connection()
	###############QUERY FOR Received HISTORY
	c.execute("SELECT * FROM User")
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("history.html", data = data, text = "Received History")

@app.route('/history/sent')
def history_sent():
	c, conn = connection()
	###############QUERY FOR Sent HISTORY
	c.execute("SELECT * FROM User")
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("history.html", data = data, text = "Sent History")

@app.route('/history/')
def history_page():
	c, conn = connection()
	###############QUERY FOR OVERALL HISTORY
	c.execute("SELECT * FROM User")
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("history.html", data = data, text = "Overall History")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")




@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        print("inside register page")
        if request.method == "POST" :
            username  = form.username.data.upper()
            email = form.email.data
            department = form.department.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM User WHERE user_id = (%s)",[thwart(username)])

            if int(x) > 0:
                print ("That username is already taken, please choose another")
                return render_template('sign-up.html', form=form, condition="Username already exists.")

            else:
                c.execute("INSERT INTO User (user_id, password, email_id, department) VALUES (%s,%s,%s,%s)",
                	[ thwart(username), thwart(password), thwart(email), thwart(department)])
                conn.commit()
                print("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['userid'] = username
                session['email'] = email
                return redirect(url_for('home'))
        print ("Nothing happened")
        return render_template("sign-up.html", form=form , condition = "Register for New User!" )
    except Exception as e:
        print (str(e))
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

            data = c.execute("SELECT * FROM User WHERE user_id = (%s)",
                             [thwart(request.form['username'].upper())])

            data = c.fetchone()
            password = data[1]
            email = data[2]
            userid = data[0]

            if sha256_crypt.verify(request.form['password'], password):
                session['logged_in'] = True
                session['userid'] = request.form['username'].upper()
                session['email'] = email
                print (session['username'])
                print ("You are now logged in")
                return redirect(url_for("home"))
            else:
                error = "Invalid credentials, try again."
                print (error)
        c.close()
        conn.close()
        gc.collect()
        return render_template("sign-in.html", error=error)
    except Exception as e:
        error = "Invalid credentials, try again."
        print (error)
        return render_template("sign-in.html", error = error)



@app.route("/logout/")
@login_required
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for('home'))

if __name__ =="__main__":
	app.debug = True
	app.run()
