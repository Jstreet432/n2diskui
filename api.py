from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def find_packets_with_timeline(start_time, end_time, filter_expression, output_file):
    # Construct the command
    command = [
        'FindPacketsWithTimeline',
        '-s', start_time,
        '-e', end_time,
        '-f', filter_expression,
        '-o', output_file
    ]
    try:
        # Run the command
        subprocess.run(command, check=True)
        return True, f"Packets saved to {output_file}"
    except subprocess.CalledProcessError as e:
        return False, str(e)
