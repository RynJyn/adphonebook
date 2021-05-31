import cgi
import os
import Cookie
import ldap
import win32com,win32com.client

form = cgi.FieldStorage()

if form.getvalue('name') and form.getvalue('password'):  
    uri = "LDAP://127.0.0.1"
    user = "CN="+form.getvalue('name')+",CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk"
    password = form.getvalue('password')
    ldapClient = ldap.initialize(uri)
    ldapClient.set_option(ldap.OPT_REFERRALS, 0)
    try:
        ldapClient.simple_bind_s(user,password)
        cookie = Cookie.SimpleCookie()
        cookie['username'] = form.getvalue('name')
        cookie['password'] = form.getvalue('password')
        print cookie
        print "Location: ./"
        print "Content-type: text/html"
        print ""
    except:
        print "Location: ./?i=1"
        print "Content-type: text/html"
        print ""
else:
    print "Location: ./"
    print "Content-type: text/html"
    print ""
