import requests
import pdb
import time 
# Твой API-ключ Яндекс
API_KEY = 'КЛЮЧ'
YANDEX_GEOCODER_URL = 'https://geocode-maps.yandex.ru/1.x/'

def get_coordinates(address):
    """Получить координаты по адресу с помощью Яндекс Геокодера"""
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(YANDEX_GEOCODER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['GeoObjectCollection']['featureMember']:
            # Извлекаем координаты
            pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            lon, lat = pos.split()
            return lat, lon
    return None, None


def load_from_dictanory_file():
    with open("data/library_adress_DCUT.txt", "r",encoding="utf-8") as library:
        temp = library.readlines()
    return temp


def add_word_dictanary_dcut(adress,lat,lon):
    with open("data/library_adress_DCUT.txt","a",encoding="utf-8") as library:
        library.write(f"{adress};['{lat}','{lon}']\n")

def processing_from_list_to_dict():
    library = load_from_dictanory_file()
    dict = {}
    for word in library:
        parts = word.split(";")
        dict[parts[0]]=parts[1]
    return dict
    
def process_data(file_path):
    """Обрабатываем данные, заменяя адреса на координаты и записывая результат в txt"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    count_requests = 0
    transformed_data = []
    dict = processing_from_list_to_dict()
    for line in lines:
        parts = line.split(';')
        # Проверяем, что строка содержит хотя бы 2 элемента
        if len(parts) > 2:
            address = parts[0].strip()  
            if address != "None" and address and (address  in dict):

                list_coordinates=dict[address].rstrip().strip("[]").replace("'","").split(",")
                
                lat = list_coordinates[0]
                lon = list_coordinates[1]
                parts[0] = f"{lat}, {lon}"  # Заменяем адрес на координаты

            elif address != "None" and address and (address not in dict) and (count_requests<700):  

                lat, lon = get_coordinates(address)
                
                if lat and lon:
                    parts[0] = f"{lat}, {lon}"  # Заменяем адрес на координаты
                add_word_dictanary_dcut(address,lat,lon)
                count_requests +=1
                print (count_requests)
               
        transformed_data.append(';'.join(parts))
        #time.sleep(1)
    # Записываем обновленные данные в текстовый файл
    with open('transformed_data.txt', 'w', encoding='utf-8') as output_file:
        for line in transformed_data:
            output_file.write(line)

# Пример использования
process_data('output_structure.txt')
