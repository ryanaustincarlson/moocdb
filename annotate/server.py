
import os, sys

try:
    from itty import *
except:
    sys.stderr.write("It looks like itty isn't installed! Install from https://github.com/toastdriven/itty\n")
    sys.exit(2)

import extract_text, submit_annotations

@get('/')
def start(request):
    return open('extract_text.html').read()

@post('/extract_text')
def extract_text_post(request):
    username = request.POST.get('username', None)
    query = request.POST.get('query', None)
    config_contents = request.POST['config'].file.read()

    basedir = extract_text.run(username, query)

    serverside_configfile = open(os.path.join(basedir, 'annotation.conf'), 'w')
    serverside_configfile.write(config_contents)
    serverside_configfile.close()

    html = open('submit_annotations.html').read() % (basedir, basedir, username)
    return html

@post('/submit_annotations')
def submit_annotations_post(request):
    username = request.POST.get('username', None)
    basedir = request.POST.get('basedir', None)

    submit_annotations.run(basedir)

    return "Done! Check the database, your annotations should be uploaded!"

run_itty(host='0.0.0.0')
