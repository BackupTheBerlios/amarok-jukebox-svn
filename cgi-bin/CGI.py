import sys, os.path
sys.path += [ os.path.abspath(os.path.basename(sys.argv[0]) + '/..') ]
import cgitb; cgitb.enable()

def httpHeaders():
    print "Content-Type: text/html; charset='utf-8'"
    print "Cache-Control: no-cache"
    print

def htmlHead():
    print "<html xmlns='http://www.w3.org/1999/xhtml'>"
    print """<head>
<title>Amarok Mserv</title>
</head>""" 
    print "<body>"

def htmlTail():
    print "</html>"

