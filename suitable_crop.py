import csv

class Crop:
    def __init__(self, name, temp_range, moisture_range, pH_range, light_intensity_range):
        self.name = name
        self.temp_range = temp_range
        self.moisture_range = moisture_range
        self.pH_range = pH_range
        self.light_intensity_range = light_intensity_range

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
            crop = Crop(name, temp_range, (moisture_min, moisture_max), (pH_min, pH_max),
                        (light_intensity_min, light_intensity_max))
            crops.append(crop)
    return crops

def identify_best_suited_crops(sensor_data, crops):
    best_crops = []
    unsuitable_reasons = {}
    for crop in crops:
        unsuitable_reasons[crop.name] = []
        if not (crop.temp_range[0] <= sensor_data.temperature <= crop.temp_range[1]):
            unsuitable_reasons[crop.name].append("Temperature out of range")
        if (crop.moisture_range[0] is not None and sensor_data.moisture < crop.moisture_range[0]):
            unsuitable_reasons[crop.name].append("Moisture too low")
        if (crop.moisture_range[1] is not None and sensor_data.moisture > crop.moisture_range[1]):
            unsuitable_reasons[crop.name].append("Moisture too high")
        if (crop.pH_range[0] is not None and sensor_data.pH < crop.pH_range[0]):
            unsuitable_reasons[crop.name].append("pH too low")
        if (crop.pH_range[1] is not None and sensor_data.pH > crop.pH_range[1]):
            unsuitable_reasons[crop.name].append("pH too high")
        if (crop.light_intensity_range[0] is not None and sensor_data.light_intensity < crop.light_intensity_range[0]):
            unsuitable_reasons[crop.name].append("Light intensity too low")
        if (crop.light_intensity_range[1] is not None and sensor_data.light_intensity > crop.light_intensity_range[1]):
            unsuitable_reasons[crop.name].append("Light intensity too high")
        
        if not unsuitable_reasons[crop.name]:
            best_crops.append(crop.name)

    
    for crop in best_crops:
        del unsuitable_reasons[crop]

    return best_crops, unsuitable_reasons


class SensorData:
    def __init__(self, temperature, moisture, pH, light_intensity):
        self.temperature = temperature
        self.moisture = moisture
        self.pH = pH
        self.light_intensity = light_intensity

def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        last_data_index = len(lines) - 6 
        last_data = lines[last_data_index:last_data_index+6]

        temperature = float(last_data[0].split(':')[1].strip())
        moisture = float(last_data[1].split(':')[1].strip())
        pH = float(last_data[2].split(':')[1].strip())
        light_intensity = float(last_data[5].split(':')[1].strip())
    return SensorData(temperature, moisture, pH, light_intensity)


def main():
    crops = read_crop_data('crop_data.csv')
    sensor_data = read_sensor_data('sensor_data.txt')
    best_crops, unsuitable_reasons = identify_best_suited_crops(sensor_data, crops)
    print("Best-suited crops based on sensor data:")
    if best_crops:
        print("Best-suited crops:")
        for crop in best_crops:
            print(crop)
    else:
        print("No suitable crops found.")
    print("\nUnsuitable reasons for each crop:")
    for crop, reasons in unsuitable_reasons.items():
        print(f"{crop}: {', '.join(reasons)}")

if __name__ == "__main__":
    main()
