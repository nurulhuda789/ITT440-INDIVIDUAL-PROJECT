import socket
import getpass
import poplib
import ssl
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

pop3 = socket.socket()

print('\n\n\n################################-SELAMAT DATANG KE *POP3 SERVER*-####################################\n')

user_email = input('Masukkan user email seperti  *****@gmail.com : ')
password = getpass.getpass('Masukkan Kata Laluan : ')

pop3 = poplib.POP3_SSL('pop.gmail.com','995')
pop3.set_debuglevel(1)
#welcome message from server
mesejDariServer = pop3.getwelcome().decode('utf-8')
print(pop3.getwelcome().decode('utf-8'))

#account authentication
pop3.user(user_email)
pop3.pass_(password)
print('Berjaya masuk ke POP3 Server')

#stat
print(' Mesej: %s. Saiz: %s' %pop3.stat())
#list
resp, emails, octets = pop3.list()
print(emails)
print('')

#charset 
def charset(msg):
    charset = msg.get_charset()
    if charset is None:
       content_type = msg.get('Content-Type', '').lower()
       pos = content_type.find('charset=')
       if pos >= 0:
          charset = content_type[pos + 8:].strip()
    return charset

#retrieve
i = len(emails)
resp, lines, octets = pop3.retr(i)
contentMessage = b'  \r\n'.join(lines).decode("utf-8")
#parse the email object to a message object
msg = Parser().parsestr(contentMessage)

print(' Baca email...')
email_from = msg.get('From')
email_to = msg.get('To')
email_subject = msg.get('Subject')
print(' >>From: ' + email_from)
print('   To: ' + email_to)
print('   Subject: ' + email_subject)

content_type = msg.get_content_type() 
#if plain text or html content type.
if content_type=='text/html':
    #email content
    content = msg.get_payload()
    #content string charset
    charset = charset(msg)
    #decode the content with charset if provided
    print('' +msg.get_payload())
    print('')
else:
    print('   Gagal untuk dapatkan content email\n')

#delete 
pop3.dele(i)
print(' <<--Mesej ini dipadam-->>\n')

#reset
pop3.rset()
print(' ***Mesej yang dipadam dapat semula***\n ')

#quit
pop3.quit()
print(' POP3 CLOSE')
print('\n\n##################################--TAMAT--#############################################')
pop3.close()
