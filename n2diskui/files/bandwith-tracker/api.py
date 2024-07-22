import json
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# Run vnstat command and capture output
result = subprocess.run(['vnstat', '-i', 'enp4s0', '-h', '--json'], stdout=subprocess.PIPE)
data = json.loads(result.stdout)

# Extract relevant data
hours = data['interfaces'][0]['traffic']['hour']

# Create a list to store processed data
processed_data = []

for hour in hours:
    date = hour['date']
    time = hour['time']
    rx = hour['rx']
    
    # Combine date and time into a single datetime object
    datetime_str = f"{date['year']}-{date['month']:02d}-{date['day']:02d} {time['hour']:02d}:{time['minute']:02d}"
    processed_data.append({'datetime': datetime_str, 'rx': rx})

# Create DataFrame
df = pd.DataFrame(processed_data)
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M')
df.set_index('datetime', inplace=True)

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['rx'])
plt.xlabel('Time')
plt.ylabel('Received Bytes')
plt.title('Network Receive Bytes Over Time')
plt.grid(True)
plt.show()

# Save data to JSON
df.reset_index()[['datetime', 'rx']].to_json('/path/to/rx_bytes.json', orient='records', date_format='iso')