# -*- coding: utf-8 -*-
# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
# -*- coding: utf-8 -*-
import pandas as pd
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from tabulate import tabulate
import matplotlib.pyplot as plt
import csv

# Define these once; use them twice!
strFrom = 'From mail address'
strTo = 'to mail address'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'
html = '''<html>
<head>
<style>
  table, th, td, p {{ border: 1px solid black; border-collapse: collapse; color: black;}}
  th, td {{ padding: 5px; }}
</style>
</head>
<body>
{table}
<br><img src="cid:image1"><br>
</body>
</html>
'''

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('html')
msgRoot.attach(msgAlternative)
differ="<br><br>"
# To open the example.csv file and read it in to data

with open('./sample.csv') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)
    msg = '{differ}{lst}'.format(header=differ, lst=data)

with open('./sample1.csv') as input_file:
    reader_1 = csv.reader(input_file)
    data += list(reader_1)

# To read the particular fields in the exmaple.csv fields and plot the bar graph and save it on the desktop as sample.png
# IMP sample.png is over-rided every time the code is compiled
fields = ['Name', 'Value']
s = pd.read_csv('sample.csv', skipinitialspace=True, usecols=fields)
s.plot(x="Name", y="Value", kind="bar")
plt.savefig('./image3.png')

# This example assumes the image is in the current directoryprint()
with open("image3.png", 'rb') as f:
    msgImage = MIMEImage(f.read())
    f.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

# to convert the csv data into the table form
html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

# allocating the parameters to the message attribute in order to send them to the mailbody
message = MIMEMultipart(
    "alternative", None, [MIMEText(html, 'html'), MIMEText(html_1, 'html')])

# Send the email (this example assumes SMTP authentication is required)
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login('logi_if', 'password')
server.sendmail(strFrom, strTo, message.as_string())
server.quit()