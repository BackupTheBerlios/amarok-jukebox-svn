import sys, os.path

def httpHeaders():
    h = "Content-Type: text/html; charset='utf-8'\n"
    h += "Cache-Control: no-cache\n\n"
    return h

def htmlHead(params = { }):
    h = """<?xml version=\"1.0\"?>
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"""
    h += "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>"
    h += """<head>
<title>amaroK juKebok</title>"""
    if params.has_key('style'):
        for s in params['style']:
            h+= "<link rel='stylesheet' type='text/css' href='%s' />" % s
    h += "</head>"
    h += "<body>"
    return h

def htmlTail():
    h = "<hr /><addressing><a href='..'>Home</a></address>"
    h += "</body>"
    h += "</html>"
    return h
