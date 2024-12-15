import getpass

import imaplib
import poplib
import pprint

GOOGLE_IMAP_SERVER = "imap.googlemail.com"
IMAP_SERVER_PORT = 993


def check_email(user,password):
    mailbox = imaplib.IMAP4_SSL(GOOGLE_IMAP_SERVER,IMAP_SERVER_PORT)
    mailbox.login(user,password)
    mailbox.select('Inbox')
    tmp,data = mailbox.search(None,"All")
    for num in data[0].split():
        tmp,data = mailbox.fetch(num,'(RFC822)')
        print('Email :{0}'.format(num))
        pprint.pprint(data[0])
    mailbox.close()
    mailbox.logout()

def chek_mail_with_pop3(user,password):
        mailbox = poplib.POP3_SSL("pop.googlemail.com",995)
        mailbox.user(user)
        mailbox.pass_(password)
        num_message = len(mailbox.list()[1])
        print("total email : {0}".format(num_message))

if __name__ == '__main__':
    user = input("enter email account : ")
    print(user)
    password = input("enter password: ")
    check_email(user,password)