import cgi
import win32com, win32com.client
import ldap
import base64
import Cookie
import os
import adlookup
form = cgi.FieldStorage()

if not 'HTTP_COOKIE' in os.environ:
  print "Location: ./?i=2"
print "Content-type: text/html"
print ""

cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
attrs = adlookup.getUserDetails("LDAP://CN="+cookie['username'].value+",CN=Users,DC=co2516,DC=ceps,DC=uclan,DC=ac,DC=uk")
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Edit Profile</title>"
print "<link rel='stylesheet' type='text/css' href='style.css'/>"
print "</head>"
print "<body>"
print "<header>"
print "<nav>"
print "<h3><a href='./'>Phonebook</a></h3>"
print "<ul>"
print "<li>"+cookie['username'].value+"</li>"
print "<li><a href='edit.py'>Edit Profile</a></li>"
print "<li><a href='logout.py'>Logout</a></li>"
print "</ul>"
print "<nav>"
print "</header>"
print "<main>"
print "<form name='editProfileForm' action='update.py' method='GET'>"
try:
  print "<img src='data:image/png;base64,"+base64.b64encode(attrs['thumbnailPhoto'])+"'/>"
except:
  print "<img src'images/users/default.jpg'/>"
print "<h2>"+cookie['username'].value+"</h2>"
print "<table id='attrTable'>"
print "<tr><p>Alter your details:</p></tr>"
print "<tr><td>Forename: </td><td><input type='text' name='forename' placeholder='"+attrs['givenName']+"'/></td></tr>"
print "<tr><td>Surname: </td><td><input type='text' name='surname' placeholder='"+attrs['sn']+"'/></td></tr>"
print "<tr><td>Phone Number: </td><td><input type='text' name='number' placeholder='"+attrs['telephoneNumber']+"'/></td></tr>"
print "</table>"
print "<p><input type='submit' value='Update'/></p>"
print "</form>"
print "</main>"
print "</body>"
print "</html>"
