import smtplib, sys, ssl, argparse, os
from ntpath import join
from collections import namedtuple
from email.mime.text import MIMEText

MessageInfo = namedtuple('MessageInfo', [
		'server',
		'port',
		'sender',
		'password',
		'receivers',
		'url'
	])

def init_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("server", type=str, help="SMTP server address")
	parser.add_argument("-p", "--port", type=int, default=465, help="SMTP server port, default: 465")
	parser.add_argument("sender_email", metavar='sender-email', type=str, help="Email address from send message")
	parser.add_argument("sender_password", metavar='sender-password', type=str, help="Sender email password")
	parser.add_argument("url", type=str, help="Url for APK")
	parser.add_argument("receivers_emails", metavar='receivers-emails', nargs="*", help="Email addreses for notification")


	args=parser.parse_args()
	if args.port < 0:
		message = "Port can't be lower that 0"
		raise Exception(message)
	return MessageInfo(args.server, args.port, args.sender_email, args.sender_password, args.receivers_emails, args.url)

def sendMessage(messageInfo):

	mail = """
	<!doctype html>	<html> <body> <p><a href="{url}">Here</a> you can download new version of application</p> </body> </html>

	<html>
  	<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>New Application available</title>
    </heade>
    <body>
    <p><a href="{url}">Here</a> you can download new version of application</p>
    </body>""".format(url = messageInfo.url)

	message = MIMEText(mail, 'html')
	message['Subject'] = 'New app available'
	message['From'] = messageInfo.sender
	message['To'] = ', '.join(messageInfo.receivers)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(messageInfo.server, int(messageInfo.port), context=context) as server:
		server.login(messageInfo.sender, messageInfo.password)
		server.sendmail(messageInfo.sender, messageInfo.receivers, message.as_string())
		server.quit()

if __name__ == "__main__":
	try:
		messageInfo = init_arg_parser()
		sendMessage(messageInfo)
	except Exception as err:
		print(err)
		sys.exit(2)
	else:
		print("Message sent to " + ', '.join(messageInfo.receivers))
