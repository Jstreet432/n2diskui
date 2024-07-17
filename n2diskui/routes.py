from flask import render_template, request, jsonify
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

@app.route('/filter_verify_return_pcap', methods=['POST'])
def clean_form_download_file():
    app.logger.info(request.json)
    pcap_filter_form = request.json['dataObj']
    timeline_directory = pcap_filter_form['timeline_directory']
    start_date = pcap_filter_form['start_date']
    end_date = pcap_filter_form['end_date']
    bpf_filter = pcap_filter_form['bpf_filter']
    save_to = pcap_filter_form['save_to']

    response = filter_create_pcap_from_timeline(timeline_directory, start_date, end_date, bpf_filter, save_to)
    app.logger.info(response)
    match response[0]:
        case True:
            message = response[1] 
            status_code = 200
        case False:
            match response[1].lower():
                case 'invalid':
                    # TODO: handle this better
                    app.logger.warning('invalid case')
                    message = f'Input Validation failed for: {response[2]}'
                    status_code = 501
                case _:
                    message = f'An error occurred when attempting to download the file. {response[1]}'
                    status_code = 500
        case _:
            raise ValueError(f'Something very strange has happened while attempting to create a pcap file from timeline files. \
                            {type(response[0])} should be a Boolean.')
       
    return jsonify(isValid=response[0], message=message), status_code