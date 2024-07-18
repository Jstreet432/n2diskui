import json
import subprocess

# Run vnstat command and capture output
result = subprocess.run(['vnstat', '-i', 'eth0', '-h', '--json'], stdout=subprocess.PIPE)
data = json.loads(result.stdout)

# Extract relevant data
hours = data['interfaces'][0]['traffic']['hour']
