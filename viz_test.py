import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Open your current file
ds = xr.open_dataset("era5-land_climate-data_Oct2024_26.1-92.8.grib", engine='cfgrib')

# Convert from Kelvin to Celsius for temperature
ds['t2m_celsius'] = ds['t2m'] - 273.15

# Calculate monthly average 2m temperature
avg_temp = ds['t2m_celsius'].mean(dim='time')

# Create a simple plot of average temperature
plt.figure(figsize=(12, 5))
temp_plot = avg_temp.isel(step=0).plot(cmap='RdBu_r')
plt.title('Average 2m Temperature (°C) - October 2024')
plt.colorbar(temp_plot, label='Temperature (°C)')
plt.savefig('avg_temperature_map.png', dpi=300, bbox_inches='tight')
plt.close()

# Calculate total monthly precipitation (convert from m to mm)
total_precip = ds['tp'].sum(dim='time') * 1000  # Convert to mm

# Create a precipitation map
plt.figure(figsize=(12, 5))
precip_plot = total_precip.isel(step=0).plot(cmap='Blues')
plt.title('Total Precipitation (mm) - October 2024')
plt.colorbar(precip_plot, label='Precipitation (mm)')
plt.savefig('total_precipitation_map.png', dpi=300, bbox_inches='tight')
plt.close()

print("Maps saved to avg_temperature_map.png and total_precipitation_map.png")