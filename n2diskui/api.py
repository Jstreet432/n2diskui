import requests
import jsonify
from datetime import datetime
import subprocess
import os
# This proxy import gives us autocomplete when referencing app
from flask import current_app as app
from flask import send_file, abort

DOWNLOADABLE_FILE_DIR = f"{app.config['BASE_DIR']}/n2diskui/files"

def filter_create_pcap_from_timeline(timeline_directory, start_date, end_date, bpf_filter, save_to):
    
    match save_to:
        case "server":
            save_to = f'{datetime.now()}.pcap'
        case "pc":
            # will download to user pc
            save_to = "NOT IMPLEMENTED YET"

    output_file = f'{DOWNLOADABLE_FILE_DIR}/{save_to}'

    # Construct the command
    command = [
        'npcapextract',
        '-t', timeline_directory,
        '-b', start_date,
        '-e', end_date,
        '-o', output_file,
        '-f', bpf_filter
        
    ]
    try:
        # Run the command
        result = subprocess.run(command, check=True)
        return True, f"Packets saved to {output_file}, {result.stdout}"
    except subprocess.CalledProcessError as e:
        app.logger.error(f'There was an error indexing the packet. {e}')
        return False, str(e)

def get_file_download(filename):
    file_path = None
    try:
        if not os.path.exists(DOWNLOADABLE_FILE_DIR):
            raise NotADirectoryError

        file_path = os.path.join(DOWNLOADABLE_FILE_DIR, filename)

        if not os.path.isfile(file_path):
            raise FileNotFoundError

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


if __name__ == "__main__":
    filter_create_pcap_from_timeline("/home/storage/","2024-06-27 00:00:00", "2024-07-30 12:00:00", "host 192.168.1.151", "output.pcap")