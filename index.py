import ldap
import cgi
import win32com,win32com.client
import base64
import Cookie
import adlookup
import os

form = cgi.FieldStorage()

if form.getvalue('name'):
  cookie = Cookie.SimpleCookie()
  cookie['username'] = form.getvalue('name')
  print cookie
print "Content-type: text/html"
print ""
print ""

print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Phonebook</title>"
print "<link rel='stylesheet' type='text/css' href='style.css'>"
print "</head>"
print "<body>"

if((form.getvalue('name') and form.getvalue('password')) or "HTTP_COOKIE" in os.environ):
  cookie_string=os.environ.get('HTTP_COOKIE')
  c=Cookie.SimpleCookie()
  c.load(cookie_string)
  uri = "LDAP://127.0.0.1"
  user = "CN="+c['username'].value+",CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk"
  password = c['password'].value
  ldapClient = ldap.initialize(uri)
  ldapClient.set_option(ldap.OPT_REFERRALS, 0)
  try:
    ldapClient.simple_bind_s(user,password)
 
    ##Main body
    print "<header>"
    print "<nav>"
    print "<h3><a href='./'>Phonebook</a></h3>"
    print "<ul>"
    print "<li>" + c['username'].value + "</li>"
    print "<li><a href='edit.py'>Edit Profile</a></li>"
    print "<li><a href='logout.py'>Logout</a></li>"
    print "</ul>"
    print "<nav>"
    print "</header>"
    print "<main>"
    print "<table>"
    print "<tr>"
    print "<td>Photo</td>"
    print "<td>Username</td>"
    print "<td>Forename</td>"
    print "<td>Surname</td>"
    print "<td>Phone Number</td>"
    print "</tr>"
   
    results = ldapClient.search_s("CN=StandardUsers,CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk", ldap.SCOPE_BASE)
    for result in results:
      result_dn = result[0]
      result_attrs = result[1]

      if "member" in result_attrs:
        for member in sorted(result_attrs["member"], key=str.lower):
          attrs = adlookup.getUserDetails("LDAP://"+member)
          try:
            username = attrs['cn']
          except:
            username = "nil"
          try:
            firstname = attrs['givenName']
          except:
            firstname = "nil"
          try:
            surname = attrs['sn']
          except:
            surname = "nil"
          try:
            phone = attrs['telephoneNumber']
          except:
            phone = "0000"
          print "<tr>"
          try:
            print "<td><img src='data:image/png;base64,"+base64.b64encode(attrs['thumbnailPhoto'])+"'></td>"
          except:
            print "<td><img src='images/users/default.jpg'></td>"
          print "<td>"+username+"</td>"
          print "<td>"+firstname+"</td>"
          print "<td>"+surname+"</td>"
          print "<td>"+phone+"</td>"
          print "</tr>"
          print "</p>"
    print "</table>"
    print "</main>"

    ldapClient.unbind_s()
  except ldap.INVALID_CREDENTIALS:
    print "Wrong password"
  except ldap.SERVER_DOWN:
    print "Server unreachable"
  
else:
  print "<form id='loginForm' name='login' action='check-login.py' method='post'>"
  print "<p>Use the form below to log in:</p>"
  print "<p>Enter username: <input type='text' name='name' autocomplete='off'></p>"
  print "<p>Enter password: <input type='password' name='password'></p>"
  if form.getvalue('i'):
    if form.getvalue('i') == '1':
      print "<p id='err'>Username or password incorrect.</p>"
    if form.getvalue('i') == '2':
      print "<p id='err'>You have been logged out. Please log in again.</p>"
    if form.getvalue('i') == '3':
      print "<p>You have been logged out successfully.</p>"
  print "<input type='submit' value='Log in'>"
  print "</form>"
print "</body>"
print "</html>"
