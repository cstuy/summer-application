from flask import Flask,session,render_template,redirect,request,url_for


app = Flask(__name__)

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    
    return "HELLO"

@app.route("/login")
def login():
    return "LOGIN"

@app.route("/logout")
def logout():
    session.pop('user',None)
    return "LOGIN"

app.secret="hello world"
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=8000)
