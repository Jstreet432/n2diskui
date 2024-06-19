import requests
import jsonify
import subprocess
import os
# This proxy import gives us autocomplete when referencing app
from flask import current_app as app
from flask import send_file, abort

DOWNLOADABLE_FILE_DIR = f"{app.config['BASE_DIR']}/n2diskui/files"

def find_packets_with_timeline(start_time, end_time, filter_expression, output_file):
    output_file = f'{DOWNLOADABLE_FILE_DIR}/{output_file}'
    # Construct the command
    command = [
        'FindPacketsWithTimeline',
        '-b', start_time,
        '-e', end_time,
        '-o', output_file,
        '-f', filter_expression
        
    ]
    try:
        # Run the command
        subprocess.run(command, check=True)
        return True, f"Packets saved to {output_file}"
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