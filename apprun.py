from flask import *
from flask_mail import Mail, Message
import random
import secrets
from flask_mysqldb import MySQL
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'starkonnect_users'

mysql = MySQL(app)
app.secret_key = secrets.token_bytes(16)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'startkonnect4@gmail.com'
app.config['MAIL_PASSWORD'] = 'startkonnect1234'
app.config['MAIL_USE-TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == "POST":
        if request.form['name']!="" and request.form['email']!="" and request.form['password']!="":
            ver_email = request.form['email']
            session['email'] = ver_email
            
            reg = None
            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM users WHERE email = '"+session.get('email')+"'")
                reg = cur.fetchone()
                print(reg,session.get('email'))
                mysql.connection.commit()
                cur.close()
            except:
                print(reg,session.get('email'))
            if reg is None:
                otp_gen = random.randint(100000,999999)
                session['otp'] = otp_gen
                print("verify")
                print(session.get('otp'))
                msg="Your One Time Password for Starkonnect is: "+str(session.get('otp'))
                message = Message("OTP Verification",sender="email",recipients=[session.get('email')])
    
                message.body = msg
    
                mail.send(message)
    
                success = "Message Sent"
    
                session['name'] = request.form.get('name')
                session['password'] = request.form['password']
    
                return render_template("otpverification.html",success=success)
            else:
                flash('This Email is already registered')
                return render_template("login.html")
        else:
            flash('Please enter all the details properly!')
            return render_template("login.html")

@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    if request.method == "POST":
        otp_enter = request.form['otp']
        if len(otp_enter)<1:
            otp_enter = -1
        if int(otp_enter)==session.get('otp'):
            return render_template("select.html")
        else:
            if otp_enter==-1:
                flash(u"New OTP is sent to {0}".format(session.get('email')))
            else:
                flash(u"Incorrect OTP\nTry Again!")
            return render_template("otpverification.html")

@app.route('/resend_verify', methods=['GET','POST'])
def resend_verify():
    if request.method == "POST":
        #email = request.form['email']
        otp_gen = random.randint(100000,999999)
        session['otp'] = otp_gen
        print("resend")
        print(session.get('otp'))
        msg="Your One Time Password for Starkonnect is: "+str(session.get('otp'))
        message = Message("OTP Verification",sender="startkonnect4@gmail.com",recipients=[session.get('email')])

        message.body = msg

        mail.send(message)

        success = "Message Sent"

        return render_template("otpverification.html",success=success)


@app.route('/selection',methods=['GET','POST'])
def selection():
    if request.method=='POST':
        chkbox = request.form.getlist('chkbox')
        session['profile'] = chkbox[0]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users VALUES('"+session.get('name')+"','"+session.get('email')+"','"+str(datetime.now())+"','"+session.get('profile')+"','"+session.get('password')+"')")
        mysql.connection.commit()
        cur.close()
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM jobs_posted")
        # jobs = cur.fetchall()
        # mysql.connection.commit()
        # cur.close()
        # lis = list()
        # i=1
        # for ele in jobs:
        #     dic = dict()
        #     dic['id'] = i
        #     dic['company'] = ele[0]
        #     dic['logo'] = ele[1]
        #     dic['new'] = ele[2]
        #     dic['featured'] = ele[3]
        #     dic['position'] = ele[4]
        #     dic['role'] = ele[5]
        #     dic['level'] = ele[6]
        #     dic['postedAt'] = ele[7]
        #     dic['contract'] = ele[8]
        #     dic['location'] = ele[9]
        #     dic['languages'] = ele[10].split(',')
        #     dic['tools'] = ele[11].split(',')
        #     i+=1
        #     lis.append(dic)
        if session.get('profile')=="freelancer":
            return render_template("homepage.html")
        elif session.get('profile')=="startup":
            return render_template("homepage-startup.html")
    
@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        if request.form['loginemail'] != "" and request.form['loginpass'] != "":
            email = request.form['loginemail']
            session['email'] = email
            session['password'] = request.form['loginpass']
            reg = None
            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM users WHERE email = '"+session.get('email')+"'")
                reg = cur.fetchone()
                session['name'] = reg[0]
                session['profile'] = reg[3]
                mysql.connection.commit()
                cur.close()
            except:
                pass
            if reg is None:
                flash('This Email is not registered')
                return render_template("login.html")
            else:
                jobs = ()
                if session.get('password')==reg[4]:
                #     cur = mysql.connection.cursor()
                #     cur.execute("SELECT * FROM jobs_posted")
                #     jobs = cur.fetchall()
                #     mysql.connection.commit()
                #     cur.close()
                #     lis = list()
                #     i=1
                #     for ele in jobs:
                #         dic = dict()
                #         dic['id'] = i
                #         dic['company'] = ele[0]
                #         dic['logo'] = ele[1]
                #         dic['new'] = ele[2]
                #         dic['featured'] = ele[3]
                #         dic['position'] = ele[4]
                #         dic['role'] = ele[5]
                #         dic['level'] = ele[6]
                #         dic['postedAt'] = ele[7]
                #         dic['contract'] = ele[8]
                #         dic['location'] = ele[9]
                #         dic['languages'] = ele[10].split(',')
                #         dic['tools'] = ele[11].split(',')
                #         i+=1
                #         lis.append(dic)
                    if session.get('profile')=="freelancer":
                        return render_template("homepage.html")
                    elif session.get('profile')=="startup":
                        return render_template("homepage-startup.html")
                else:
                    flash('Incorrect Password')
                    return render_template('login.html')
        else:
            flash('Please enter all the details properly!')
            return render_template("login.html")

@app.route('/myprofile',methods=['GET','POST'])
def myprofile():
    if request.method=="POST":
        profile = ""
        found = False
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT Profile FROM users WHERE email = '"+session.get('email')+"'")
            profile = cur.fetchone()[0]
            mysql.connection.commit()
            cur.close()
        except:
            profile = ""
        try:
            cur = mysql.connection.cursor()
            if profile=="freelancer":
                cur.execute("SELECT name FROM userprofiles WHERE email = '"+session.get('email')+"'")
            elif profile=="startup":
                cur.execute("SELECT name FROM startup_profiles WHERE email = '"+session.get('email')+"'")
            if cur.fetchone()[0]:
                found = True
            mysql.connection.commit()
            cur.close()
        except:
             pass
        if profile=="freelancer":
            if found:
                return render_template("Freelancer-Profile.html")
            else:    
                return render_template("Freelancer.html")
        elif profile=="startup":
            if found:
                return render_template("Startup-Profile.html")
            else:
                return render_template("Startup.html")
        print(profile)
        
@app.route('/viewprofile/<prof>',methods=['GET','POST'])
def viewprofile(prof):
    if request.method=="POST":
        if prof=="freelancer":
            session['dob'] = request.form['dob']
            session['mob'] = request.form['Mobile_Number']
            genbox = request.form.getlist('Gender')
            session['gender'] = genbox[0]
            session['city'] = request.form['city']
            session['pincode'] = request.form['pincode']
            session['state'] = request.form['State']
            session['country'] = request.form['Country']
            try:
                cur = mysql.connection.cursor()
                #print("INSERT INTO userprofiles VALUES('"+session.get('name')+"','"+session.get('dob')+"','"+session.get('email')+"','"+session.get("mob")+"','"+session.get('gender')+"','"+session.get('city')+"','"+session.get('pincode')+"','"+session.get('state')+"','"+session.get('country')+"')")
                cur.execute("INSERT INTO userprofiles VALUES('"+session.get('name')+"','"+session.get('dob')+"','"+session.get('email')+"','"+session.get("mob")+"','"+session.get('gender')+"','"+session.get('city')+"','"+session.get('pincode')+"','"+session.get('state')+"','"+session.get('country')+"')")
                mysql.connection.commit()
                cur.close()
            except Exception as e:
                print(e)
            
        elif prof=="startup":
            session['domain'] = request.form['Company_Domain']
            session['number'] = request.form['Contact_Number']
            session['website'] = request.form['Website']
            session['city'] = request.form['City']
            session['pincode'] = request.form['Pin_Code']
            session['state'] = request.form['State']
            session['country'] = request.form['Country']
            try:
                cur = mysql.connection.cursor()
                print("INSERT INTO startup_profiles VALUES('"+session.get('name')+"','"+session.get('domain')+"','"+session.get('email')+"','"+session.get("number")+"','"+session.get('website')+"','"+session.get('pincode')+"','"+session.get('city')+"','"+session.get('state')+"','"+session.get('country')+"')")
                cur.execute("INSERT INTO startup_profiles VALUES('"+session.get('name')+"','"+session.get('domain')+"','"+session.get('email')+"','"+session.get("number")+"','"+session.get('website')+"','"+session.get('pincode')+"','"+session.get('city')+"','"+session.get('state')+"','"+session.get('country')+"')")
                mysql.connection.commit()
                cur.close()
                print("Added")
            except Exception as e:
                print(e)
        if prof=="freelancer":
            return render_template("homepage.html")
        elif prof=="startup":
            return render_template("homepage-startup.html")
    
@app.route('/myapp',methods=['GET','POST'])
def myapp():
    if request.method=="POST":
        return render_template("Freelancer-Applications.html")
        
@app.route('/jobsposted',methods=['GET','POST'])
def jobsposted():
    if request.method=="POST":
        return render_template("Jobsposted.html")

@app.route('/Createjob',methods=['GET','POST'])
def Createjob():
    if request.method=="POST":
        return render_template("Create-Vacancy.html")
    
@app.route('/homebt/<profi>',methods=['GET','POST'])
def homebt(profi):
    if request.method=="POST":
        if profi=="freelancer":
            return render_template("homepage.html")
        elif profi=="startup":
            return render_template("homepage-startup.html")
        
@app.route('/applyjob/<company>',methods=['GET','POST'])
def applyjob(company):
    if request.method=="POST":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM jobs_posted WHERE company = '"+company+"'")
        jobcom = cur.fetchone()
        mysql.connection.commit()
        cur.execute("SELECT * FROM jobs_applied WHERE company = '"+company+"'")
        jobcheck = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if jobcheck:
            if jobcheck[0]==session.get('email') and jobcheck[2]==company and jobcheck[3]==jobcom[4]:
                flash("You have already applied for the position of "+jobcom[4]+" at "+company+" as "+jobcom[8])
                return render_template("homepage.html")
            else:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO jobs_applied VALUES ('"+session.get('email')+"','"+session.get('name')+"','"+company+"','"+jobcom[4]+"','"+jobcom[5]+"','"+jobcom[6]+"','"+jobcom[8]+"')")
                mysql.connection.commit()
                cur.close()
                flash("You have successfully applied for the position of "+jobcom[4]+" at "+company+" as "+jobcom[8])
                return render_template("homepage.html")
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO jobs_applied VALUES ('"+session.get('email')+"','"+session.get('name')+"','"+company+"','"+jobcom[4]+"','"+jobcom[5]+"','"+jobcom[6]+"','"+jobcom[8]+"')")
            mysql.connection.commit()
            cur.close()
            flash("You have successfully applied for the position of "+jobcom[4]+" at "+company+" as "+jobcom[8])
            return render_template("homepage.html")
        
    
if __name__ == '__main__':
    app.run()
