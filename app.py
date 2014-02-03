from flask import Flask,session,render_template,redirect,request,url_for,flash
import db 
import json,os

app = Flask(__name__,static_folder="applications")

@app.route("/",methods=['GET','POST'])
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    
    questions = db.getanswers(session['user'])


    if request.method=="GET":
        for q in questions['questions']:
            if q['name']=='email':
                q['answer']=session['user']
                
        return render_template("index.html",questions=questions)

    # POST
    f =request.form
    if f['button']=="Cancel and logout":
        return redirect(url_for('logout'))
    for q in questions['questions']:
        if f.has_key(q['name']):
            q['answer']=f[q['name']]


    for f in request.files:
        dirname="applications/"+session['user']
        try:
            os.mkdir(dirname)
        except:
            pass
        
        file = request.files[f]
        qname=f
        filename=file.filename
        for q in questions['questions']:
            if q['name']==qname and filename != "":
                q['answer']=filename
                file.save(dirname+"/"+qname)

    db.updateanswers(session['user'],questions)
    flash("Application updated and saved")
    return redirect(url_for("index"))

@app.route("/changepassword")
def changepassword():
    return "Change Password"

@app.route("/forgotpassword")
def forgotpassword():
    return "Forgot Password"


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
        
    # post
    button = request.form['button']
    if button=='register':
        return redirect(url_for('register'))
    email=request.form['email']
    password=request.form['password']
    result = db.checkCredentials(email,password)
    if result==False:
        flash("Invalid username or password")
        return render_template('login.html')
    
    session['user']=email
    return redirect(url_for('index'))
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')

    # POST
    d=request.form
    button=d['button']
    if button=='Home':
        return redirect(url_for('index'))

    email=d['email']
    password=d['password']
    cpassword=d['cpassword']
    if (password!=cpassword):
        flash("Passwords don't match")
        return render_template('register.html')
    result = db.addUser(email,password)
    if result==None:
        flash("Couldn't create account")
        return render_template("register.html")
    
    return redirect(url_for('login'))
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

app.secret_key="hello world"
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=8000)
