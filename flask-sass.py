import os.path
from subprocess import Popen, PIPE
from flask import Response, abort

from imaginary_app import app
from imaginary_app.settings import STATIC_PATH, SASS_PATH # Add these to your settings

# Helper
def scss(data):
    sass = Popen([SASS_PATH, '--trace', '--scss', '--stdin'],
                 stdin=PIPE, stdout=PIPE, stderr=PIPE)
    sass.stdin.write(data)
    sass.stdin.flush()
    sass.stdin.close()
    sass.wait()

    css = sass.stdout.read()
    error = sass.stderr.read()

    if len(css) > 0:
        return True, css
    else:
        return False, error

# Sample route
@app.route('/static/css/<name>.css')
def css(name):
    scss_path = os.path.join(STATIC_PATH, 'css/%s.scss' % name)

    if not os.path.exists(scss_path):
        return abort(404)

    with open(scss_path) as fd:
        success, body = scss(fd.read())

    if success:
        return Response(body, status=200, content_type='text/css')
    else:
        return Response('<pre>%s</pre>', status=500, content_type='text/html')

