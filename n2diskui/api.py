from datetime import datetime
import subprocess
import os
import re
from typing import Tuple
# This proxy import gives us autocomplete when referencing app
from flask import current_app as app
from flask import send_file, abort, Response

DOWNLOADABLE_FILE_DIR = f"{app.config['BASE_DIR']}/n2diskui/files"

def filter_create_pcap_from_timeline(timeline_directory: str, start_date: str, end_date: str, bpf_filter: str, save_to: str) -> Tuple[bool,str]:
    verify_dict = _verify_filter_input(timeline_directory, start_date, end_date)
    message = 'invalid'
    failed_input = [k for k, v in verify_dict.items() if not v]
    if failed_input:
        return False, message, failed_input
    
    match save_to:
        case "server":
            save_to = f'{datetime.now()}.pcap'
        case "pc":
            # will download to user pc
            save_to = "NOT IMPLEMENTED YET"

    output_file = f'{DOWNLOADABLE_FILE_DIR}/{save_to}'

    #TODO: BPF VERIFICATION

    command = [
        'npcapextract',
        '-t', timeline_directory,
        '-b', start_date,
        '-e', end_date,
        '-o', output_file,
        '-f', bpf_filter
        
    ]
    try:
        result = subprocess.run(command, check=True)
        # TODO: result is succesful but bpf filter did not return a result.
        return True, f"Packet capture saved to the server at {output_file}"
    except subprocess.CalledProcessError as e:
        app.logger.error(f'There was an error indexing the packet. {e}')
        return False, str(e)

def get_file_download(filename: str) -> Response:
    file_path = None
    try:
        if not os.path.exists(DOWNLOADABLE_FILE_DIR):
            raise NotADirectoryError()

        file_path = os.path.join(DOWNLOADABLE_FILE_DIR, filename)

        if not os.path.isfile(file_path):
            raise FileNotFoundError()

        response = send_file(file_path, as_attachment=True)
        response.headers['Content-Disposition'] = f'attachement; filename={filename}'

        return response
        
    except FileNotFoundError:
        app.logger.error(f'File {filename} not found.  {file_path} is missing!')
        abort(404)
    except NotADirectoryError:
        app.logger.error(f'Directory {DOWNLOADABLE_FILE_DIR} does not exist!')
        abort(500)
    except Exception as e:
        if not file_path: file_path = 'File path was not found.'
        app.logger.error(f'Error occurred when user attempted to download a file: \n {file_path} \n {e} ')
        abort(500)
    
def _verify_filter_input(timeline_directory, start_date, end_date):
    verified_dict = {}
    # TODO: Timeline directory needs a whole lot of work to verify it is a valid timeline directory
    verified_dict['timeline_directory'] = True
    # Verify Dates
    date_pattern = '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    verified_dict['start_date'] = re.match(date_pattern, start_date) is not None
    verified_dict['end_date'] = re.match(date_pattern, end_date) is not None
    return verified_dict


if __name__ == "__main__":
    filter_create_pcap_from_timeline("/home/storage/","2024-06-27 00:00:00", "2024-07-30 12:00:00", "host 192.168.1.151", "output.pcap")