import CGI

# FIXME: As this is updated, Debug.py should also be modified
Version = "0.6"

def serve(request):
    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()

    doc += "<p>This is amaroK-juKebox " + Version + ".</p>"
    doc += "<p>For more recent versions, see the <a href='http://amarok-jukebox.berlios.de/'>home page</a>.</p>"

    doc += CGI.htmlTail()

    request.serve_string(doc)
