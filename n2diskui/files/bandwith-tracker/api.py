import json
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# Run vnstat command and capture output
result = subprocess.run(['vnstat', '-i', 'wlp5s0', '-d', '--json'], stdout=subprocess.PIPE)
data = json.loads(result.stdout)

# Extract relevant data
days = data['interfaces'][0]['traffic']['day']

# Create a list to store processed data
processed_data = []

for day in days:
    date = day['date']
    rx = day['rx']
    
    # Combine date into a single string
    datetime_str = f"{date['year']}-{date['month']:02d}-{date['day']:02d}"
    processed_data.append({'date': datetime_str, 'rx': rx})

# Create DataFrame
df = pd.DataFrame(processed_data)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.set_index('date', inplace=True)
print(df)

# Save data to JSON
df.to_json('here.json', orient='records')
