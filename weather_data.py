import openmeteo_requests
import pandas as pd

# Initialize the Open Meteo API client
openmeteo = openmeteo_requests.Client()

# Define the parameters for the API request
params = {
    "latitude": 30.3244,
    "longitude": 78.0339,
    "start_date": "2024-04-03",
    "end_date": "2025-04-08",  # Extend the end date by one year
    "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
              "wind_speed_10m_mean", "wind_speed_10m_max", "cloud_cover_mean",
              "shortwave_radiation_sum", "relative_humidity_2m_mean",
              "relative_humidity_2m_max", "relative_humidity_2m_min",
              "precipitation_sum", "rain_sum", "snowfall_sum",
              "pressure_msl_mean", "soil_moisture_0_to_10cm_mean"]
}

# Make the API request
response = openmeteo.weather_api("https://climate-api.open-meteo.com/v1/climate", params=params)

# Process the response
for location_response in response:
    print(f"Location: {location_response.Latitude()}°N, {location_response.Longitude()}°E")
    print(f"Elevation: {location_response.Elevation()} m asl")
    print(f"Timezone: {location_response.Timezone()} ({location_response.TimezoneAbbreviation()})")
    print(f"Timezone difference to GMT+0: {location_response.UtcOffsetSeconds()} s")
    
    # Process daily data
    daily_data = location_response.Daily()
    daily_df = pd.DataFrame({
        "Date": pd.to_datetime(daily_data.Time(), unit="s"),
        "Mean Temperature (2m)": daily_data.Variables(0).ValuesAsNumpy(),
        "Max Temperature (2m)": daily_data.Variables(1).ValuesAsNumpy(),
        "Min Temperature (2m)": daily_data.Variables(2).ValuesAsNumpy(),
        "Mean Wind Speed (10m)": daily_data.Variables(3).ValuesAsNumpy(),
        "Max Wind Speed (10m)": daily_data.Variables(4).ValuesAsNumpy(),
        "Mean Cloud Cover": daily_data.Variables(5).ValuesAsNumpy(),
        "Shortwave Radiation Sum": daily_data.Variables(6).ValuesAsNumpy(),
        "Mean Relative Humidity (2m)": daily_data.Variables(7).ValuesAsNumpy(),
        "Max Relative Humidity (2m)": daily_data.Variables(8).ValuesAsNumpy(),
        "Min Relative Humidity (2m)": daily_data.Variables(9).ValuesAsNumpy(),
        "Precipitation Sum": daily_data.Variables(10).ValuesAsNumpy(),
        "Rain Sum": daily_data.Variables(11).ValuesAsNumpy(),
        "Snowfall Sum": daily_data.Variables(12).ValuesAsNumpy(),
        "Sealevel Pressure": daily_data.Variables(13).ValuesAsNumpy(),
        "Mean Soil Moisture (0-10cm)": daily_data.Variables(14).ValuesAsNumpy()
    })
    
    # Save daily data to a CSV file
    daily_df.to_csv(f"{location_response.Latitude()}_{location_response.Longitude()}_weather_data.csv", index=False)
