import json
def process_file(filename):
    data = []
    organization = None
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Пропускаем пустые строки
            if not line:
                continue

            # Если строка заканчивается точкой с запятой и содержит только одно разделение, это организация
            if line.endswith(';') and line.count(';') == 1:
                # Завершаем предыдущую организацию, если она есть
                if organization:
                    data.append(organization)
                
                # Начинаем новую организацию
                organization = {
                    'name': line.strip(';'),  # Убираем точку с запятой
                    'locations': []
                }
            else:
                # Иначе это строка с координатами и описаниями
                parts = line.split(';')
                if len(parts) >= 3:
                    coordinates = parts[0].split(',')
                    if len(coordinates) == 2:
                        try:
                            lat, lon = map(float, coordinates)  # Преобразуем координаты в числа
                            location = {
                                'latitude': lat,
                                'longitude': lon,
                                'description1': parts[1].strip(),
                                'description2': parts[2].strip()
                            }
                            organization['locations'].append(location)
                        except ValueError:
                            print(f"Некорректные данные для координат: {coordinates}")
                    else:
                        print(f"Некорректная строка для координат: {parts[0]}")
    
    # Добавляем последнюю организацию
    if organization:
        data.append(organization)

    # Сохраняем результат в JSON
    with open('data/output.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

# Пример использования
process_file('data/transformed_data.txt')
