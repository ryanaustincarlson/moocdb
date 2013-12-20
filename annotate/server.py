
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

if parser.get_default('url') == args.url and parser.get_default('port') == args.port:
    if not sys.argv[0].startswith("./"):
        script_call = "python " 
    script_call += "%s -h" % sys.argv[0]

    sys.stderr.write("LOG: It looks like you're using the default parameters for the BRAT server location (%s:%s).\nLOG: Run `%s` for more details.\n\n" % (args.url, args.port, script_call))
        

run_itty(host='0.0.0.0')
