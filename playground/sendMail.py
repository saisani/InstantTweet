import smtplib

gmail_user = 'fall8731@gmail.com'
gmail_password = '2much2kill'


sent_from = gmail_user
to = ['trigger@applet.ifttt.com']
subject = '#IFTTT'
body = "Hey, blah up?\n\n- You"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

print(email_text)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print 'Email sent!'
except:
    print 'Something went wrong...'