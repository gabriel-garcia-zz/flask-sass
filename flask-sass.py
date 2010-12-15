import os.path
from subprocess import Popen, PIPE
from flask import Response, abort

from imaginary_app import app
from imaginary_app.settings import STATIC_PATH, SASS_PATH # Add these to your settings

# Helper
def scss(data, load_path):
    args = ['--trace', '--scss', '--stdin', '-I', load_path]
    sass = Popen([SASS_PATH] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
    dir_path = os.path.join(STATIC_PATH, 'css')
    scss_path = os.path.join(dir_path, '%s.scss' % name)

    if not os.path.exists(scss_path):
        return abort(404)

    with open(scss_path) as fd:
        success, body = scss(fd.read(), dir_path)

    if success:
        return Response(body, status=200, content_type='text/css')
    else:
        return Response('<pre>%s</pre>' % body, status=500, content_type='text/html')

