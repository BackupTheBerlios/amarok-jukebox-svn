import sys, os.path
sys.path += [ os.path.abspath(os.path.basename(sys.argv[0]) + '/../..') ]
import cgitb; cgitb.enable()

def httpHeaders():
    print "Content-Type: text/html; charset='utf-8'"
    print "Cache-Control: no-cache"
    print

def htmlHead():
    print """<?xml version=\"1.0\"?>
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"""
    print "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>"
    print """<head>
<title>amaroK juKebok</title>
</head>""" 
    print "<body>"

def htmlTail():
    print "<hr /><addressing><a href='..'>Home</a></address>"
    print "</body>"
    print "</html>"
