import os
import csv
import json
from data import source_path, destination_path

amenities = []


def infer_type(id_usage1, id_usage2, id_usage3):
    if id_usage1 == 'A' and id_usage2 == '4' and (id_usage3 == '59' or id_usage3 == '69' or id_usage3 == '136'):
            # Épiceries, supermarchés, fruiteries
            return 'FOOD_STORE'
    return None


with open(os.path.join(source_path, 'occupation-commerciale-2022.csv'), 'r', encoding='utf-8', newline='') as data_file:
    reader = csv.reader(data_file)
    next(reader, None)
    for row in reader:
        ID, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ID_USAGE1, USAGE1, ID_USAGE2, USAGE2, ID_USAGE3, USAGE3, _, _, _, _, VACANT_A_LOUER, _, _, _, _, _, _, _, _, _, _, _, _, _, LAT, LONG = row
        if VACANT_A_LOUER.lower() == 'oui':
            continue
        amenity_type = infer_type(ID_USAGE1, ID_USAGE2, ID_USAGE3)
        if not amenity_type:
            continue

        amenity = {
            'type': amenity_type,
            'position': {
                'lat': float(LAT),
                'lng': float(LONG),
            }
        }
        amenities.append(amenity)


os.makedirs(destination_path, exist_ok=True)
with open(os.path.join(destination_path, 'amenities.json'), 'w', encoding='utf-8') as output_file:
    json.dump(amenities, output_file)
