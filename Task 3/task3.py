import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

api_url = 'https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=50.4547&longitude=30.5238&start_date=2024-08-01&end_date=2024-09-12&hourly=temperature_2m'

# Fetch weather data from the API
response = requests.get(api_url)
data = response.json()

# Create a DataFrame
df = pd.DataFrame(data)
timestamps = df.loc[df['hourly_units'] == 'iso8601', 'hourly'].values[0]
temperatures = df.loc[df['hourly_units'] == '°C', 'hourly'].values[0]

df = pd.DataFrame({
    'Date': timestamps,
    'Temperature (°C)': temperatures
})

df['Date'] = df['Date'].apply(lambda x:datetime.strptime(x,'%Y-%m-%dT%H:%M')) 

# Save DataFrame to CSV
csv_file = 'temperature_change_Kyiv.csv'
df.to_csv(csv_file, index=False)
max_idx = df['Temperature (°C)'].idxmax()
min_idx = df['Temperature (°C)'].idxmin()

# Plot data
plt.figure(figsize=(10, 5))

plt.plot(df['Date'], df['Temperature (°C)'], marker='o', linestyle='-', color='g')

# Highlighting max temperature
plt.scatter(df['Date'].iloc[max_idx], df['Temperature (°C)'].iloc[max_idx], color='r')
plt.text(df['Date'].iloc[max_idx], df['Temperature (°C)'].iloc[max_idx], f'Max: {df["Temperature (°C)"].iloc[max_idx]}°C', 
         color='r', ha='center', va='bottom')

# Highlighting min temperature
plt.scatter(df['Date'].iloc[min_idx], df['Temperature (°C)'].iloc[min_idx], color='b')
plt.text(df['Date'].iloc[min_idx], df['Temperature (°C)'].iloc[min_idx], f'Min: {df["Temperature (°C)"].iloc[min_idx]}°C', 
         color='b', ha='center', va='top')

plt.title(f'Temperature changes for Kyiv between {df["Date"].min()} and {df["Date"].max()}')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image
plt.savefig('temperature_change_Kyiv.png')

plt.show()