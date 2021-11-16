import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

frommail = "from@email.address"
to = "toniodupcc@gmail.com"


msg = MIMEMultipart('alternative')
msg['Subject'] = "AMP Email"
msg['From'] = frommail
msg['To'] = to

#Email body.
plain_text = "Hi,\nThis is the plain text version of this Email.\nHere is a link that is for testing:\nhttps://amp.dev/documentation/guides-and-tutorials/start/create_email/?format=email"


html = """\
<html>
  <head>
  <meta charset="utf-8">    
</head>
  <body>
    <p>Hi!<br>
    <h1>Hello, I am an HTML MAIL!</h1>
    </p>
  </body>
</html>
"""


html_amp = """\
<html amp4email>
  <head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
  <style amp-custom>
    h1 {
      margin: 1rem;
    }
  </style>
</head>
  <body>
    <p>Hi!<br>
    <h1>Hello, I am an AMP EMAIL!</h1>
    </p>
  </body>
</html>
"""

#Important: Some email clients only render the last MIME part, so it is
#recommended to place the text/x-amp-html MIME part before the text/html.
part1 = MIMEText(plain_text, 'plain')
part2 = MIMEText(html_amp, 'x-amp-html')
part3 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)
msg.attach(part3)

s = smtplib.SMTP('localhost')
s.sendmail(frommail, to, msg.as_string())
s.quit()