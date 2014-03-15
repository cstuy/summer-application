# Import smtplib for the actual sending function
import smtplib
import db

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email(user,message):
    msg = MIMEText(message)
    msg['Subject'] = 'Password reminder'
    msg['From'] = "no-reply@cstuy.org"
    msg['To'] = user
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], user, msg.as_string())
    s.quit()

def send_confirmation(user,questions):
    message="Submission for %s\n--------------\n"%(user)
    for q in questions['questions']:
        message = message + q['label']+" : "+q['answer']+"\n--------------------\n"
    send_email(user,message)

def send_password(u):
    user=db.getCredentials(u)
    if user==None:
        return
    m="Your password (for this email address) is: %s"%(user['password'])
    send_email(u,m)


if __name__=="__main__":
    send_password("zamansky@gmail.com")
