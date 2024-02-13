import idna
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import utils

raw_sender_email: str
sender_password: str

email_choice = input('Choose sender email (red\green): ')

if email_choice == 'red':
    raw_sender_email = 'احمر@فريق-٤.البحرين'
    sender_password = '0357417254'
elif email_choice == 'green':
    raw_sender_email = 'اخضر@فريق-٤.البحرين'
    sender_password = '9334304501'
else:
    raise ValueError('Invalid email choice')


local_sender, domain_sender = raw_sender_email.split('@')
normalized_sender_domain = idna.encode(domain_sender).decode('ascii')
normalized_sender_local = idna.encode(local_sender).decode('ascii')
normalized_sender_email = f'{normalized_sender_local}@{normalized_sender_domain}'

print(f'raw sender email: {raw_sender_email}')
print(f'normalized sender Email: {normalized_sender_email}')

raw_reciever_email = input('Enter reciever email: ')

local_reciever, domain_reciever = raw_reciever_email.split('@')
normalized_reciever_domain = idna.encode(domain_reciever).decode('ascii')
normalized_reciever_email = f'{local_reciever}@{normalized_reciever_domain}'

print(f'raw receiver email: {raw_reciever_email}')
print(f'normalized receiver Email: {normalized_reciever_email}')


subject = input('Enter subject: ')
body = input('Enter body: ')



message = MIMEMultipart()
message['From'] = normalized_sender_email
message['To'] = normalized_reciever_email

message['Subject'] = Header(subject, 'ascii')
message.attach(MIMEText(body, "plain"))


smtp_server = "xn--ngbof4h.xn--mgbam8grabl.xn--mgbcpq6gpa1a"
smtp_server_password = 'HTinwm#KL5x2'
smtp_port = 587

# Create an SMTP session
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.command_encoding = 'utf-8'
    # Start the TLS connection (for secure communication)
    # server.starttls()

    # Log in to your email account
    server.login(normalized_sender_email, sender_password)

    # Send the email
    server.sendmail(normalized_sender_email, normalized_reciever_email, message.as_string())

print("Email sent successfully!")