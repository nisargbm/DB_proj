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
def index():
	if(session.get('logged_in')):
		if(session['logged_in']):
			return redirect(url_for('home'))
	return redirect(url_for('homepage'))
	
@app.route('/homepage')
def homepage():
	if(session.get('logged_in')):
		if(session['logged_in']):
			return redirect(url_for('home'))
	return render_template("homepage.html")


@app.route('/track/<variable>')
@login_required
def track_doc(variable):
	try:
		c, conn = connection()
		c.execute("SELECT doc_id,sender,receiver,subject,details,date_of_receipt,status,comment FROM Document NATURAL JOIN Document_details NATURAL JOIN Process WHERE doc_id = (%s) AND user_id = receiver AND movement_date = date_of_receipt ORDER BY date_of_receipt DESC;",[thwart(variable)])
		conn.commit()
		data = c.fetchall()
		return render_template("doc_track.html", data = data)
	except Exception as e:
		print (str(e))
		return(str(e))

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
	c.execute("SELECT DISTINCT doc_id,subject,details,sender FROM Process NATURAL JOIN Document NATURAL JOIN Document_details WHERE user_id = (%s) AND status = 'PENDING' AND receiver = (%s) AND movement_date = date_of_receipt;",[thwart(session['userid']),thwart(session['userid'])])
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("home.html", data=data)



@app.route('/upload/')
@login_required
def upload():
	return render_template("upload.html")
	
@app.route('/existing_doc/<variable>', methods=["GET","POST"])
@login_required
def existing_doc(variable):
	try:
		c, conn = connection()
		c.execute("SELECT sender,doc_id,subject,organisation,details,number_of_documents FROM Document_details NATURAL JOIN Document WHERE doc_id=(%s) AND receiver=(%s)",[thwart(variable), session['userid']])
		conn.commit()
		doc_details = c.fetchone()	
		if request.method == "POST" :
			sender  = session['userid'];
			comments = request.form.get('comment')
			receiver = request.form.get('to')
			doc_id = variable
			if(request.form.get('status')):
				status = "ACCEPTED"
			else:
				status = "REJECTED"

			c.execute("INSERT INTO Process(user_id,doc_id) VALUES((%s),(%s));", [thwart(receiver),thwart(doc_id)])
			conn.commit()
			c.execute("INSERT INTO Document(doc_id,sender,receiver) VALUES ((%s),(%s),(%s));", [thwart(doc_id), thwart(sender), thwart(receiver)])
			conn.commit()
			c.execute("UPDATE Process SET status = (%s), comment = (%s) WHERE doc_id = (%s) AND user_id = (%s) AND status = 'PENDING';",[thwart(status),thwart(comments),thwart(doc_id), thwart(sender)])
			conn.commit()
			c.execute("UPDATE Document SET date_of_receipt = NOW() WHERE doc_id = (%s) AND sender = (%s) AND receiver = (%s);",[thwart(doc_id),thwart(sender),thwart(receiver)])
			conn.commit()

			print("Thanks for uploading!")
			c.close()
			conn.close()
			gc.collect()
			return redirect(url_for('home'))

		c.execute("SELECT DISTINCT department FROM User WHERE department<>'OTHERS'")
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
		return render_template("existing_doc.html", users = users, dept = dept, doc_details = doc_details)
	except Exception as e:
		print (str(e))
		return(str(e))

@app.route('/my_docs/')
@login_required
def my_docs():
	c, conn = connection()
	c.execute("SELECT doc_id,subject,details FROM Process NATURAL JOIN Document_details WHERE user_id = (%s) AND status= 'CREATED' ORDER BY movement_date DESC;",[thwart(session['userid'])])
	conn.commit()
	data = c.fetchall()
	c.close()
	conn.close()
	gc.collect()
	return render_template("my_docs.html", data = data)


class InwardNewForm(Form):
	to = TextField('to')
	user_id = TextField('user_id')
	subject = TextField('subject',[validators.Length(min = 1, max = 255)])
	document_details = TextField('document_details',[validators.Length(min = 1, max = 1000)])
	organization = TextField('organization',[validators.Length(min = 1, max = 1000)])
	no_docs = TextField('no_docs')
	# place = TextField('place_of_recieving',[validators.Length(min = 1,max = 1000)]) 

@app.route('/new_doc/', methods=["GET","POST"])
@login_required
def new_doc():
	try:
		c, conn = connection()
		form = InwardNewForm(request.form)
		if request.method == "POST" :
			sender  = session['userid']
			subject = form.subject.data
			doc_details = form.document_details.data
			org = form.organization.data
			no_docs = form.no_docs.data
			reciever = form.to.data
			# place = form.place.data

			c.execute("INSERT INTO Document_details( subject, number_of_documents, details, organisation ) VALUES (%s, %s, %s, %s)",[ thwart(subject), thwart(no_docs), thwart(doc_details), thwart(org)])
			data = c.execute("SELECT doc_id FROM Document_details WHERE subject= (%s) AND number_of_documents = (%s) AND details = (%s) AND organisation = (%s)",[ thwart(subject), thwart(no_docs), thwart(doc_details) , thwart(org)])
			data = c.fetchone()
			doc_id1=data[0]
			print("HEllo"+str(reciever))
			c.execute("INSERT INTO Process(user_id,doc_id,status) VALUES (%s,%s,'CREATED')",[session['userid'], int(doc_id1)])
			c.execute("INSERT INTO Process(user_id,doc_id) VALUES (%s,%s)",[thwart(reciever), int(doc_id1)])
			c.execute("INSERT INTO Document(doc_id,sender,receiver)VALUES(%s,%s,%s)",[int(doc_id1),session['userid'],thwart(reciever)])
			conn.commit()
			print("Thanks for uploading!")
			c.close()
			conn.close()
			gc.collect()
			return redirect(url_for('home'))
		else:
			c.execute("SELECT DISTINCT department FROM User WHERE department<>'OTHERS'")
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

@app.route('/database/', methods=["GET","POST"])
def database():
	if request.method == "POST":
		if request.form.get("password") == "12345":
			c, conn = connection()
			data = ""
			name = ""
			if request.form.get("query"):
				c.execute(request.form.get("query"))
				conn.commit
				name = c.description
				data = c.fetchall()
			c.execute("SELECT * FROM User")
			conn.commit()
			User = c.fetchall()
			c.execute("SELECT * FROM Process")
			conn.commit()
			Process = c.fetchall()
			c.execute("SELECT * FROM Document")
			conn.commit()
			Document = c.fetchall()
			c.execute("SELECT * FROM Document_details")
			conn.commit()
			Document_details = c.fetchall()
			c.close()
			conn.close()
			gc.collect()
			return render_template("database.html", status="logged_in", User = User, Process = Process, Document = Document, Document_details = Document_details, data = data, name = name)
	return render_template("database.html", status="login" )

@app.route('/history/received')
def history_recieved():
    history_cat = "received"
    return render_template("history.html", history_cat = history_cat)

@app.route('/new_outward_form/', methods=["GET","POST"])
@login_required
def new_outward_form():
	try:
		c, conn = connection()
		form = InwardNewForm(request.form)		
		if request.method == "POST" :
			sender  = session['userid'];
			subject = form.subject.data
			doc_details = form.document_details.data
			org = form.organization.data
			no_docs = form.no_docs.data
			reciever = form.to.data
			# place = form.place.data
			send_place = request.form.get("sending_place")
			to_whom = request.form.get("to_whom")
			c.execute("INSERT INTO Document_details( subject, number_of_documents, details, organisation ) VALUES (%s, %s, %s, %s)",[ thwart(subject), thwart(no_docs), thwart(doc_details), thwart(org)])
			data = c.execute("SELECT doc_id FROM Document_details WHERE subject= (%s) AND number_of_documents = (%s) AND details = (%s) AND organisation = (%s)",[ thwart(subject), thwart(no_docs), thwart(doc_details) , thwart(org)])
			data = c.fetchone()
			doc_id1=data[0]
			c.execute("INSERT INTO Process(user_id,doc_id,status) VALUES (%s,%s,'CREATED')",[session['userid'], int(doc_id1)])
			c.execute("INSERT INTO Process(user_id,doc_id) VALUES (%s,%s)",[thwart(reciever), int(doc_id1)])
			c.execute("INSERT INTO Document(doc_id,sender,receiver)VALUES(%s,%s,%s)",[int(doc_id1),session['userid'],thwart(reciever)])
			conn.commit()
			print("Thanks for uploading!")
			
			c.execute("INSERT INTO Outward (sending_place, to_whom_addressed) VALUES (%s,%s)",[ thwart(send_place), thwart(to_whom)])
			conn.commit()
			c.close()
			conn.close()
			gc.collect()
			return redirect(url_for('home'))
		else:
			c.execute("SELECT DISTINCT department FROM User WHERE department<>'OTHERS'")
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
			return render_template("new_outward_form.html",form=form, users = users, dept = dept)
	except Exception as e:
		print (str(e))
		return(str(e))


@app.route('/old_outward_form/<variable>', methods=["GET","POST"])
@login_required
def old_outward_form(variable):
	try:
		c, conn = connection()
		c.execute("SELECT sender,doc_id,subject,organisation,details,number_of_documents FROM Document_details NATURAL JOIN Document WHERE doc_id=(%s) AND receiver=(%s)",[thwart(variable), session['userid']])
		conn.commit()
		doc_details = c.fetchone()	
		if request.method == "POST" :
			sender  = session['userid'];
			comments = request.form.get("comment")
			receiver = "OTHERS"
			doc_id = variable
			if(request.form.get('status')):
				status = "ACCEPTED"
			else:
				status = "REJECTED"
			send_place = request.form.get("sending_place")
			to_whom = request.form.get("to_whom")
			post_type = request.form.get("type_of_post")
			cost = request.form.get("estimated_cost")

			print(sender,comments,receiver,doc_id,status,send_place,to_whom)

			c.execute("INSERT INTO Process(user_id,doc_id) VALUES((%s),(%s));", [thwart(receiver),thwart(doc_id)])
			conn.commit()
			c.execute("INSERT INTO Document(doc_id,sender,receiver) VALUES ((%s),(%s),(%s));", [thwart(doc_id), thwart(sender), thwart(receiver)])
			conn.commit()
			c.execute("UPDATE Process SET status = (%s), comment = (%s) WHERE doc_id = (%s) AND user_id = (%s) AND status = 'PENDING';",[thwart(status),thwart(comments),thwart(doc_id), thwart(sender)])
			conn.commit()
			c.execute("UPDATE Document SET date_of_receipt = NOW() WHERE doc_id = (%s) AND sender = (%s) AND receiver = (%s);",[thwart(doc_id),thwart(sender),thwart(receiver)])
			conn.commit()

			print("Thanks for uploading!")
			c.execute("INSERT INTO Outward (doc_id, sending_place, to_whom_addressed) VALUES (%s,%s,%s)",[ thwart(doc_id), thwart(send_place), thwart(to_whom)])
			conn.commit()
			c.close()
			conn.close()
			gc.collect()
			return redirect(url_for('home'))

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
		return render_template("old_outward_form.html", users = users, dept = dept, doc_details = doc_details)
	except Exception as e:
		print (str(e))
		return(str(e))


@app.route('/history/received/individual/', methods=["GET","POST"])
def received_individual():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            person  = request.form.get("user_id")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject, details, sender FROM Document NATURAL JOIN Document_details NATURAL JOIN Process WHERE sender = (%s) AND receiver = (%s) AND status = (%s) AND user_id = receiver;",[thwart(person), thwart(session['userid']), thwart(status)])
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT * FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("individual.html", data = data, table = table)

@app.route('/history/received/department/', methods=["GET","POST"])
def received_department():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            dept  = request.form.get("dept")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject,details, sender FROM Document NATURAL JOIN Document_details WHERE receiver = (%s) AND doc_id IN ( SELECT doc_id FROM Process WHERE status= (%s) ) AND sender IN ( SELECT user_id FROM User WHERE department = (%s) );", [thwart(session['userid']), thwart(status), thwart(dept)])
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT DISTINCT department FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("department.html", data = data, table = table)

@app.route('/history/received/overall/', methods=["GET","POST"])
def received_overall():
    c, conn = connection()
    c.execute("SELECT doc_id,subject,details,sender FROM Document_details NATURAL JOIN Document WHERE receiver = (%s);",[thwart(session['userid'])])
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("overall.html", data = data)

@app.route('/history/sent')
def history_sent():
    history_cat = "sent"
    return render_template("history.html", history_cat = history_cat)

@app.route('/history/sent/individual/', methods=["GET","POST"])
def sent_individual():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            person  = request.form.get("user_id")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject,details, receiver FROM Document NATURAL JOIN Document_details WHERE sender = (%s) AND receiver = (%s) AND doc_id IN ( SELECT doc_id FROM Process WHERE status= (%s));",[thwart(session['userid']),thwart(person),thwart(status)])
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT * FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("individual.html", data = data, table = table)

@app.route('/history/sent/department/', methods=["GET","POST"])
def sent_department():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            dept  = request.form.get("dept")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject, details,receiver FROM Document NATURAL JOIN Document_details WHERE sender = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= (%s)) AND receiver IN ( SELECT user_id FROM User WHERE department = (%s));",[thwart(session['userid']),thwart(status),thwart(dept)])
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT DISTINCT department FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("department.html", data = data, table = table)

@app.route('/history/sent/overall/', methods=["GET","POST"])
def sent_overall():
    c, conn = connection()
    c.execute("SELECT doc_id,subject,details,receiver FROM Document_details NATURAL JOIN Document WHERE sender=(%s)",[thwart(session['userid'])])
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("overall.html", data = data)

@app.route('/history/overall')
def history_overall():
    history_cat = "overall"
    return render_template("history.html", history_cat = history_cat)

@app.route('/history/overall/individual/', methods=["GET","POST"])
def overall_individual():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            person  = request.form.get("user_id")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject,details, receiver FROM Document NATURAL JOIN Document_details WHERE (sender = (%s) AND receiver = (%s)) OR (sender = (%s) AND receiver = (%s)) AND doc_id IN ( SELECT doc_id FROM Process WHERE status= (%s));",[thwart(session['userid']),thwart(person),thwart(person), thwart(session['userid'], thwart(status))]) ###################################QUERY
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT * FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("individual.html", data = data, table = table)

@app.route('/history/overall/department/', methods=["GET","POST"])
def overall_department():
    c, conn = connection()
    table = ""
    if request.method == "POST" :
            print("Getting data from form")
            dept  = request.form.get("dept")
            status  = request.form.get("status")
            c.execute("SELECT doc_id, subject, details,receiver FROM Document NATURAL JOIN Document_details WHERE sender = (%s) OR receiver = (%s) AND doc_id IN ( SELECT doc_id FROM Process WHERE status= (%s) ) AND receiver IN (SELECT user_id FROM User WHERE department = (%s));",[thwart(session['userid']),thwart(session['userid']),thwart(status),thwart(dept)])###################################QUERY
            conn.commit()
            table = c.fetchall()
            print ("table")
            print (table)
    c.execute("SELECT DISTINCT department FROM User")
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("department.html", data = data, table = table)

@app.route('/history/overall/overall/', methods=["GET","POST"])
def overall_overall():
    c, conn = connection()
    c.execute("")###################################QUERY
    conn.commit()
    data = c.fetchall()
    c.close()
    conn.close()
    gc.collect()
    return render_template("overall.html", data = data)

@app.route('/statistics/my_stats')
@login_required
def my_stats():
	status="Personal"
	c,conn = connection()
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'PENDING')",[thwart(session['userid'])])
	conn.commit()
	pending_count = c.fetchone()[0]
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'ACCEPTED')",[thwart(session['userid'])])
	conn.commit()
	accepted_count = c.fetchone()[0]
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'REJECTED')",[thwart(session['userid'])])
	conn.commit()
	rejected_count = c.fetchone()[0]
	print (pending_count,rejected_count,accepted_count)
	print (type(pending_count))
	info = [int(pending_count) , int(accepted_count) , int(rejected_count)]
	print (info)
	return render_template("stats.html", status = status ,info = info)

@app.route('/statistics/overall')
@login_required
def overall_stats():
	status="Overall"
	c,conn = connection()
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'PENDING')",[thwart(session['userid'])])
	conn.commit()
	pending_count = c.fetchone()[0]
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'ACCEPTED')",[thwart(session['userid'])])
	conn.commit()
	accepted_count = c.fetchone()[0]
	c.execute("SELECT COUNT(DISTINCT doc_id) AS totalcount FROM Document WHERE receiver = (%s) AND doc_id IN (SELECT doc_id FROM Process WHERE status= 'REJECTED')",[thwart(session['userid'])])
	conn.commit()
	rejected_count = c.fetchone()[0]
	print (pending_count,rejected_count,accepted_count)
	print (type(pending_count))
	info = [int(pending_count) , int(accepted_count) , int(rejected_count)]
	print (info)
	return render_template("stats.html", status = status)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    department = TextField('Department')
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])


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
                #print (session['username'])
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
        print (error,e)
        return render_template("sign-in.html", error = error)



@app.route("/logout/")
@login_required
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for('homepage'))

if __name__ =="__main__":
	app.debug = True
	app.run()

