import xarray as xr
import pandas as pd
import numpy as np

# File path of your GRIB file
grib_file = "era5-land_climate-data_Oct2024_26.1-92.8.grib"

# Function to convert 4D climate data to a 2D DataFrame
def convert_era5_to_dataframe(ds):
    """
    Convert an xarray Dataset of ERA5 data to a pandas DataFrame.
    Flattens the multi-dimensional data into a tabular format.
    """
    # Initialize an empty list to store records
    records = []
    
    # Get the variable names (excluding coordinates)
    var_names = list(ds.data_vars.keys())
    
    # Loop through each combination of dimensions
    for t_idx, time in enumerate(ds.time.values):
        for s_idx, step in enumerate(ds.step.values):
            for lat_idx, lat in enumerate(ds.latitude.values):
                for lon_idx, lon in enumerate(ds.longitude.values):
                    
                    # Create a record with datetime information
                    record = {
                        'time': pd.Timestamp(time).strftime('%Y-%m-%d'),
                        'step': pd.Timedelta(step).total_seconds() // 3600,  # Convert to hours
                        'latitude': lat,
                        'longitude': lon,
                        'valid_time': pd.Timestamp(ds.valid_time.values[t_idx, s_idx]).strftime('%Y-%m-%d %H:%M')
                    }
                    
                    # Add each variable's value at this point
                    for var in var_names:
                        # Handle special cases for temperature
                        if var == 't2m':
                            # Store both Kelvin and Celsius
                            kelvin_value = float(ds[var].values[t_idx, s_idx, lat_idx, lon_idx])
                            record[f'{var}_kelvin'] = kelvin_value
                            record[f'{var}_celsius'] = kelvin_value - 273.15
                        elif var == 'd2m':  # dewpoint temperature
                            kelvin_value = float(ds[var].values[t_idx, s_idx, lat_idx, lon_idx])
                            record[f'{var}_kelvin'] = kelvin_value
                            record[f'{var}_celsius'] = kelvin_value - 273.15
                        elif var == 'tp':  # precipitation
                            # Convert from meters to millimeters for easier interpretation
                            record[f'{var}_mm'] = float(ds[var].values[t_idx, s_idx, lat_idx, lon_idx]) * 1000
                        else:
                            record[var] = float(ds[var].values[t_idx, s_idx, lat_idx, lon_idx])
                    
                    records.append(record)
    
    # Convert list of records to DataFrame
    df = pd.DataFrame(records)
    return df

try:
    # Open the GRIB file
    print(f"Opening {grib_file}...")
    ds = xr.open_dataset(grib_file, engine='cfgrib')
    
    # Convert to DataFrame
    print("Converting to DataFrame...")
    df = convert_era5_to_dataframe(ds)
    
    # Print info about the DataFrame
    print("\nDataFrame information:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Print a sample of the data
    print("\nSample data (first 5 rows):")
    print(df.head())
    
    # Save to CSV
    csv_filename = grib_file.replace('.grib', '.csv')
    print(f"\nSaving to {csv_filename}...")
    df.to_csv(csv_filename, index=False)
    print(f"Data successfully saved to {csv_filename}")
    
    # Optional: Save a sample file with fewer rows for easy viewing
    sample_size = min(1000, len(df))
    sample_filename = grib_file.replace('.grib', '_sample.csv')
    df.sample(sample_size).to_csv(sample_filename, index=False)
    print(f"Sample of {sample_size} rows saved to {sample_filename}")
    
except Exception as e:
    print(f"Error: {str(e)}")