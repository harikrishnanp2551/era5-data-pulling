import xarray as xr
import matplotlib.pyplot as plt
import test

# Read the GRIB file
data = xr.open_dataset(test.custom_filename , engine='cfgrib')

# Print basic information about the dataset
print("Dataset contents:")
print(data)

# Show available variables
print("\nAvailable variables:")
for var_name in data.data_vars:
    print(f"- {var_name}")

# Let's visualize one variable (2m temperature) for the first time step
if '2t' in data.data_vars:  # ERA5 shorthand for 2m temperature
    # Select the first time step
    temp_data = data['2t'].isel(time=0)
    
    # Convert from Kelvin to Celsius
    temp_celsius = temp_data - 273.15
    
    # Create a simple plot
    plt.figure(figsize=(10, 6))
    temp_celsius.plot()
    plt.title('2m Temperature (°C)')
    plt.savefig('temperature_map.png')
    plt.close()
    print("Temperature map saved as 'temperature_map.png'")