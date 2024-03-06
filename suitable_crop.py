import csv

class Crop:
    def __init__(self, name, temp_range, moisture_range, pH_range, light_intensity_range, growing_season):
        self.name = name
        self.temp_range = temp_range
        self.moisture_range = moisture_range
        self.pH_range = pH_range
        self.light_intensity_range = light_intensity_range
        self.growing_season = growing_season

def read_crop_data(file_path):
    crops = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            temp_range = (float(row['Temp_Min']), float(row['Temp_Max']))
            moisture_min = float(row['Moisture_Min']) if row['Moisture_Min'] != 'None' else None
            moisture_max = float(row['Moisture_Max']) if row['Moisture_Max'] != 'None' else None
            pH_min = float(row['pH_Min']) if row['pH_Min'] != 'None' else None
            pH_max = float(row['pH_Max']) if row['pH_Max'] != 'None' else None
            light_intensity_min = float(row['Light_Intensity_Min']) if row['Light_Intensity_Min'] != 'None' else None
            light_intensity_max = float(row['Light_Intensity_Max']) if row['Light_Intensity_Max'] != 'None' else None
            growing_season_min = int(row['Growing_Season_Min'])
            growing_season_max = int(row['Growing_Season_Max'])
            crop = Crop(name, temp_range, (moisture_min, moisture_max), (pH_min, pH_max),
                        (light_intensity_min, light_intensity_max), (growing_season_min, growing_season_max))
            crops.append(crop)
    return crops

def identify_best_suited_crops(sensor_data, crops):
    best_crops = []
    for crop in crops:
        if (crop.temp_range[0] <= sensor_data.temperature <= crop.temp_range[1] if sensor_data.temperature is not None else True and
            (crop.moisture_range[0] is None or crop.moisture_range[0] <= sensor_data.moisture if sensor_data.moisture is not None else True) and
            (crop.moisture_range[1] is None or sensor_data.moisture <= crop.moisture_range[1] if sensor_data.moisture is not None else True) and
            (crop.pH_range[0] is None or crop.pH_range[0] <= sensor_data.pH if sensor_data.pH is not None else True) and
            (crop.pH_range[1] is None or sensor_data.pH <= crop.pH_range[1] if sensor_data.pH is not None else True) and
            (crop.light_intensity_range[0] is None or crop.light_intensity_range[0] <= sensor_data.light_intensity if sensor_data.light_intensity is not None else True) and
            (crop.light_intensity_range[1] is None or sensor_data.light_intensity <= crop.light_intensity_range[1] if sensor_data.light_intensity is not None else True) and
            crop.growing_season[0] <= sensor_data.growing_season <= crop.growing_season[1] if sensor_data.growing_season is not None else True):
            best_crops.append(crop.name)
    return best_crops

class SensorData:
    def __init__(self, temperature, moisture, pH, light_intensity, growing_season):
        self.temperature = temperature
        self.moisture = moisture
        self.pH = pH
        self.light_intensity = light_intensity
        self.growing_season = growing_season

def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()[-6:]  # Read the last 6 lines
        temperature = float(data[0].split(':')[1].strip())
        moisture = float(data[1].split(':')[1].strip())
        pH = float(data[2].split(':')[1].strip())
        light_intensity = float(data[5].split(':')[1].strip())
        growing_season = int(data[-1].split(':')[1].strip())  # Extract from the last line
    return SensorData(temperature, moisture, pH, light_intensity, growing_season)


def main():
    crops = read_crop_data('crop_data.csv')
    sensor_data = read_sensor_data('sensor_data.txt')
    best_crops = identify_best_suited_crops(sensor_data, crops)
    print("Best-suited crops based on sensor data:")
    for crop in best_crops:
        print(crop)

if __name__ == "__main__":
    main()
