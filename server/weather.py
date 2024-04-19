import requests
import json
from datetime import datetime, timedelta

# API key and base URL
api_key = "934510d317424ee5b01100420241504"
base_url = "http://api.weatherapi.com/v1/future.json"

# Function to get user input for start date and number of days
def get_input():
    start_date_str = input("Enter the starting date (YYYY-MM-DD): ")
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return get_input()
    
    num_days = int(input("Enter the number of days: "))
    return start_date, num_days

# Function to make API calls and store data
def get_weather_data(location, start_date, num_days):
    with open("weather_data.json", "w") as file:
        for i in range(num_days):
            # Format date
            date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Make API call
            params = {
                "key": api_key,
                "q": location,
                "dt": date_str
            }
            response = requests.get(base_url, params=params)
            data = response.json()
            
            # Write data to file
            json.dump(data, file)
            file.write("\n")

# Get user input
start_date, num_days = get_input()

# Get weather data
get_weather_data("Dehradun", start_date, num_days)
