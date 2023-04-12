import os
import sendgrid
import codecs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import mysql.connector
purpose='test'  #In the db, there are three columns: purpose, subject and file_name. Purpose is just a short description of the subject.
query1="select subject,file_name from twilio_files where purpose=%s" #obtaining subject and file_name for the given purpose.
db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

cursor = db.cursor()
cursor.execute(query1,(purpose,))
result=cursor.fetchall()
cursor.close()
sub=result[0][0]
src="D:/"   #This is the src file where the html files are located.
location=src+result[0][1] #final location= files_location+ result[0][1]( file name).
file = codecs.open(location, 'r')
content=file.read()

from_='xxx@yyy.io'
query2="select to_ from twilio_from_and_to_emails where from_=%s"   #selecting all the emails who have from_ as their sender in the db.
db = mysql.connector.connect(user='admin', password='X', host='X.rds.amazonaws.com',database='X')

cursor = db.cursor()
cursor.execute(query2,(from_,))
result2=cursor.fetchall()
cursor.close()
mails=[]
for i in result2:
    mails.append(i[0])  #mails contain all the sendee/reciever for the given sender.

message = Mail(
    from_email=from_,
    to_emails=mails,
    subject=sub,
    html_content=content)
try:
    sg = SendGridAPIClient('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')
    response = sg.client.tracking_settings.get()
    print(response.status_code)
    print("DONE")
except Exception as e:
    print(e)
