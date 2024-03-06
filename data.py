from datetime import datetime

class SensorData:
    def __init__(self, temperature, moisture, pH, ammonia_gas, conductivity, light_intensity):
        self.temperature = temperature
        self.moisture = moisture
        self.pH = pH
        self.ammonia_gas = ammonia_gas
        self.conductivity = conductivity
        self.light_intensity = light_intensity

def collect_sensor_data_manually():
    print("Enter sensor data:")
    temperature = float(input("Temperature (in Celsius): "))
    moisture = float(input("Moisture (in percentage): "))
    pH = float(input("pH: "))
    ammonia_gas = float(input("Ammonia Gas (in ppm): "))
    conductivity = float(input("Conductivity (in μS/cm): "))
    light_intensity = float(input("Light Intensity (in lux): "))

    return SensorData(temperature, moisture, pH, ammonia_gas, conductivity, light_intensity)

def save_sensor_data_to_file(sensor_data, filename):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(filename, 'a') as file:  # Open the file in append mode
            file.write("\nDate: {}\n".format(current_date))
            file.write("Temperature: {}\n".format(sensor_data.temperature))
            file.write("Moisture: {}\n".format(sensor_data.moisture))
            file.write("pH: {}\n".format(sensor_data.pH))
            file.write("Ammonia Gas: {}\n".format(sensor_data.ammonia_gas))
            file.write("Conductivity: {}\n".format(sensor_data.conductivity))
            file.write("Light Intensity: {}\n".format(sensor_data.light_intensity))
        print("Sensor data appended to", filename)
    except Exception as e:
        print("An error occurred while writing to the file:", e)

def main():
    # Choose whether to collect sensor data manually or through sensors
    data_source = input("Enter data source (manual/sensors): ")

    if data_source.lower() == "manual":
        # Collect sensor data manually
        sensor_data = collect_sensor_data_manually()
    elif data_source.lower() == "sensors":
        # Collect sensor data from actual sensors (to be implemented)
        # For now, use manual data entry as a placeholder
        sensor_data = collect_sensor_data_manually()
    else:
        print("Invalid data source. Please enter 'manual' or 'sensors'.")

    # Save sensor data to file
    filename = "sensor_data.txt"
    save_sensor_data_to_file(sensor_data, filename)

if __name__ == "__main__":
    main()
