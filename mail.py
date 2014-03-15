# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_password(u):
    m="hello world"
    msg = MIMEText(m)
    msg['Subject'] = 'The sub'
    msg['From'] = "no-reply@cstuy.org"
    msg['To'] = u
    s = smtplib.SMTP('localhost')
    s.sendmail("zamansky@cstuy.org", u, msg.as_string())
    s.quit()


if __name__=="__main__":
    send_password("zamansky@gmail.com")
