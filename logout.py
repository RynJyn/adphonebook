import cgi
import Cookie
import os

cookieExpired = False

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)
    try:
        c['username'].value = ""
        c['password'].value = ""
        c['username']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        c['password']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        print c
        cookieExpired = True
        print "Location: ./?i=3"
    except KeyError:
        print "The cookie was not set or has expired<br>"
else:
    cookieExpired = True
print "Content-type: text/html"
print ""
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Log Out</title>"
print "<link rel='stylesheet' type='text/css' href='style.css'/>"
print "</head>"
print "<body>"

if cookieExpired == True:
    print "<p>You have been logged out successfully.</p>"

print "</body>"
print "</html>"
