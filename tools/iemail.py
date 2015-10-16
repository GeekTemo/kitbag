__author__ = 'gongxingfa'

import getpass,poplib, email,string

m = poplib.POP3('pop.163.com')
m.user('18650090314@163.com')
m.pass_('gxf921758')
mail_count = len(m.list()[1])
for index in range(1, mail_count):
    rsp, msglines,msgsize=m.retr(index)
    mail = email.message_from_string(string.join(msglines, '\n'))
    mail_from = email.utils.parseaddr(mail['From'])[1]
    if mail_from == 'PostMaster@asiainfo.com':
        m.dele(index)
        print 'Delete ', mail_from

