import json
import re
# Функция для чтения данных из файла с координатами и адресами
def read_coordinates_file(filename):
    coordinates_map = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split(";")
            address = parts[0].strip()
            # Используем регулярное выражение для поиска координат
            match = re.search(r"\['([\d\.]+)','([\d\.]+)'\]", parts[1])
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                coordinates_map[(latitude, longitude)] = address
            else:
                print(f"Координаты не найдены в строке: {line}")
    return coordinates_map

# Функция для добавления адресов в JSON по координатам
def add_address_to_json(json_filename, coordinates_map):
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for entry in data:
        if "locations" in entry and entry["locations"]:
            for location in entry["locations"]:
                coord_tuple = (location["latitude"], location["longitude"])
                if coord_tuple in coordinates_map:
                    location["address"] = coordinates_map[coord_tuple]
                else:
                    location["address"] = "Адрес не найден"
    
    with open("data/updated_data.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Пример использования
coordinates_file = "data/library_adress_DCUT.txt"  # Ваш файл с адресами и координатами
json_file = "data/output.json"  # Ваш JSON файл

coordinates_map = read_coordinates_file(coordinates_file)
add_address_to_json(json_file, coordinates_map)
