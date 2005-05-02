import sys, os.path

def httpHeaders(type = "text/html; charset='utf-8'"):
    h = "Content-Type: %s\n" % type
    return h + "\n"

def htmlHead(params = { }):
    h = """<?xml version=\"1.0\"?>
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"""
    h += "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>"
    h += """<head>
<title>amaroK juKebox</title>"""
    if params.has_key('style'):
        for s in params['style']:
            h += "<link rel='stylesheet' type='text/css' href='%s' />" % s
    if params.has_key('markup'):
        for s in params['markup']:
            h += s
    h += "</head>"
    h += "<body>"
    return h

def htmlTail():
    h = "<hr />"
    h += "<p><a href='player'>Controls</a></p>"
    h += "<address><a href='..'>Home</a></address>"
    h += "</body>"
    h += "</html>"
    return h
