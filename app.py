from flask import Flask,session,render_template,redirect,request,url_for,flash
import db 
import json,os
from bson.json_util import dumps
import mail

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

    dirname="applications/"+session['user']
    try:
        os.mkdir(dirname)
    except:
        pass

    output = open(dirname+"/answers.json","w")
    outputstring = dumps(questions,output)
    output.write(outputstring)
    output.close()
    
    for f in request.files:
        
        file = request.files[f]
        qname=f
        filename=file.filename
        for q in questions['questions']:
            if q['name']==qname and filename != "":
                q['answer']=filename
                file.save(dirname+"/"+qname)

    
    db.updateanswers(session['user'],questions)
    mail.send_confirmation(session['user'],questions)
    flash("Application updated and saved - confirmation email sent - Remember to log out")
    return redirect(url_for("logout"))

@app.route("/changepassword")
def changepassword():
    return render_template('changepassword.html')

@app.route("/forgotpassword",methods=['GET','POST'])
def forgotpassword():
    if request.method=="GET":
        return render_template("forgot_password.html")

    # do the send the password magic here
    mail.send_password(request.form['email'])
    flash("Email sent");
    return redirect(url_for('index'))

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
        
    # post
    button = request.form['button']
    if button=="forgot":
        return redirect(url_for('forgotpassword'))



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
