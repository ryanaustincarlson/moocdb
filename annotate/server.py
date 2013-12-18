
import os, sys, argparse

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

    annotation_dir = os.path.basename(basedir)
    html = open('submit_annotations.html').read().format(url=args.url, port=args.port, annotation_dir=annotation_dir, basedir=basedir, username=username)
    return html

@post('/submit_annotations')
def submit_annotations_post(request):
    username = request.POST.get('username', None)
    basedir = request.POST.get('basedir', None)

    submit_annotations.run(basedir)

    return "Done! Check the database, your annotations should be uploaded!"

parser = argparse.ArgumentParser(description="itty server to facilitate annotations using BRAT")
parser.add_argument('-u','--url', default='127.0.0.1', help='BRAT url (default: %(default)s)', required=False)
parser.add_argument('-p','--port', default='8001', help='BRAT port (default: %(default)s)', required=False)
args = parser.parse_args()

run_itty(host='0.0.0.0')
