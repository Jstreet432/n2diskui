from flask import render_template, request
# This proxy import gives us autocomplete when referencing app
from flask import current_app as app
from n2diskui.api import get_file_download, filter_create_pcap_from_timeline

@app.route('/')
@app.route('/index')
def index():
    return render_template('FrontPage.html', title='N2DiskUI')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return get_file_download(filename)

@app.route('/filter_return_pcap', methods=['POST'])
def clean_form_download_file():
   app.logger.info(request.form)
   timeline_directory = request.form['timeline_directory']
   start_date = request.form['start_date']
   end_date = request.form['end_date']
   bpf_filter = request.form['bpf_filter']
   save_to = request.form['save_to']

   response = filter_create_pcap_from_timeline(timeline_directory, start_date, end_date, bpf_filter, save_to)

   if not response[0]:
       return "There was an error, please check your input.", 500

   return response[1], 200