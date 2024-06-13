from flask import render_template
# This proxy import gives us autocomplete when referencing app
from flask import current_app as app
from n2diskui.api import get_file_download

@app.route('/')
@app.route('/index')
def index():
    return render_template('FrontPage.html', title='N2DiskUI')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return get_file_download(filename)