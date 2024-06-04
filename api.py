from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def find_packets_with_timeline(start_time, end_time, filter_expression, output_file):
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
        return False, str(e)
