import cgi
import ldap
import os
import Cookie

form = cgi.FieldStorage()

username = ""
password = ""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)
    username = c['username'].value
    password = c['password'].value

try:
    uri = "LDAP://127.0.0.1"
    user = "CN="+username+",CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk"
    user2 = "CN=Administrator,CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk"
    pass2 = "<ADMIN_PASSWORD>"
    ldapClient = ldap.initialize(uri)
    ldapClient.set_option(ldap.OPT_REFERRALS, 0)
    ldapClient.simple_bind_s(user2, pass2)
    mod_attrs = []

    if form.getvalue('forename'):
        mod_attrs.append((ldap.MOD_REPLACE, 'givenName', form.getvalue('forename')))

    if form.getvalue('surname'):
        mod_attrs.append((ldap.MOD_REPLACE, 'sn', form.getvalue('surname')))

    if form.getvalue('number'):
        mod_attrs.append((ldap.MOD_REPLACE, 'telephoneNumber', form.getvalue('number')))

    ldapClient.modify_s("CN="+username+",CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk", mod_attrs)
    ldapClient.unbind_s()
except ldap.LDAPError as e:
    print e.message

print "Location: ./"
print "Content-type: text/html"
print ""
