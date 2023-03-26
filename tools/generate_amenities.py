import os
from data import source_path, generated_path
import csv
import json
import shapefile
import geojson
from shapely import geometry
from shapely import ops
import pyproj

amenities = {}

with open(os.path.join(source_path, 'amenities', 'businesses.csv'), 'r', encoding='utf-8', newline='') as data_file:
    reader = csv.reader(data_file)
    next(reader, None)

    for row in reader:
        _, _, _, _, _, type, statut, _, latitude, longitude, _, _ = row
        if statut.lower() != 'ouvert' or not latitude or not longitude:
            continue

        category = None
        type = type.lower()
        if type.startswith('restaurant') or type == 'casse-croûte':
            category = 'restaurant'
        elif 'épicerie' in type or type == 'supermarché':
            category = 'food_store'

        if category:
            pt = [float(longitude), float(latitude)]
            amenities.setdefault(category, []).append(pt)

with open(os.path.join(source_path, 'amenities', 'occupation-commerciale-2022.csv'), 'r', encoding='utf-8', newline='') as data_file:
    reader = csv.reader(data_file)
    next(reader, None)

    for row in reader:
        _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ID_USAGE1, _, ID_USAGE2, _, ID_USAGE3, _, _, _, _, _, VACANT_A_LOUER, _, _, _, _, _, _, _, _, _, _, _, _, _, LAT, LONG = row
        if VACANT_A_LOUER.lower() != 'non':
            continue

        category = None

        # For list of known usages, see https://data.montreal.ca/dataset/f8582c4d-a933-4306-bb27-d883e13dd207/resource/bb891287-3690-4a5a-9641-09cea02a8cc7/download/usages.csv
        if ID_USAGE1 == 'A':
            if ID_USAGE2 == '41' and ID_USAGE3 == '103':
                category = 'pharmacy'
        if ID_USAGE1 == 'F':
            if ID_USAGE2 == '46' and ID_USAGE3 == '40':
                category = 'clinic'
            elif ID_USAGE2 == '17' and ID_USAGE3 == '37':
                category = 'daycare'

        if category:
            pt = [float(LONG), float(LAT)]
            amenities.setdefault(category, []).append(pt)


with open(os.path.join(source_path, 'amenities', 'lieuxculturels.csv'), 'r', encoding='utf-8', newline='') as data_file:
    reader = csv.reader(data_file)
    next(reader, None)

    for row in reader:
        _, NomReseau, _, _, _, _, _, _, _, Longitude, Latitude, _ = row

        if NomReseau.lower() == 'bibliothèque':
            pt = [float(Longitude), float(Latitude)]
            amenities.setdefault('library', []).append(pt)

def get_all_exterior_points(polygon):
    result = []
    if polygon.geom_type == 'Polygon':
        return polygon.exterior.coords
    elif polygon.geom_type == 'MultiPolygon':
        result = []
        for part in polygon.geoms:
            result.extend(get_all_exterior_points(part))
        return result

with open(os.path.join(source_path, 'amenities', 'espace_vert.json'), 'r', encoding='utf-8', newline='') as data_file:
    parks: geojson.FeatureCollection = geojson.load(data_file)

    for feature in parks.features:
        park_type = feature.properties['TYPO1']
        if park_type and park_type.lower().startswith('parc'):
            polygon = geometry.shape(feature.geometry).simplify(0.0001)
            points = set(get_all_exterior_points(polygon))
            amenities.setdefault('park', []).extend(points)


with shapefile.Reader(os.path.join(source_path, 'amenities', 'etablissements-meq-mes-esrishp.zip/PPS_Public_Ecole.shp'), encoding='latin1') as reader:
    for shape_rec in reader.iterShapeRecords():
        level = shape_rec.record.ORDRE_ENS.lower()
        if level != 'primaire' and level != 'secondaire':
            continue
        cp = shape_rec.record.CD_POSTL_I
        if cp[0] != 'H' or cp[0:2] == 'H0' or cp[0:2] == 'H7':
            continue

        pt: geometry.Point = geometry.shape(shape_rec.shape.__geo_interface__)
        match level:
            case 'primaire':
                amenities.setdefault('primary_school', []).append([pt.x, pt.y])
            case 'secondaire':
                amenities.setdefault('secondary_school', []).append([pt.x, pt.y])

from_proj = pyproj.CRS('EPSG:2950')
to_proj = pyproj.CRS('EPSG:4326')
project = pyproj.Transformer.from_crs(
    from_proj, to_proj, always_xy=True).transform


known_stops = set()
with shapefile.Reader(os.path.join(source_path, 'amenities', 'stm_sig.zip/stm_arrets_sig.shp'), encoding='latin1') as reader:
    for shape_rec in reader.iterShapeRecords():
        if not shape_rec.record.route_id:
            continue  # not real stops
        if not any(int(x) in [1, 2, 5] for x in shape_rec.record.route_id.split(',')):
            continue  # only keep green, orange and blue metro lines
        if shape_rec.record.stop_code in [10282, 10286, 10288]:
            continue  # remove Laval orange line stations
        if shape_rec.record.stop_code in known_stops:
            continue  # skip duplicates
        known_stops.add(shape_rec.record.stop_code)

        pt: geometry.Point = geometry.shape(shape_rec.shape.__geo_interface__)
        pt = ops.transform(project, pt)
        amenities.setdefault('metro_station', []).append([pt.x, pt.y])

os.makedirs(os.path.join(generated_path, 'amenities'), exist_ok=True)
for type, items in amenities.items():
    with open(os.path.join(generated_path, 'amenities', '{}.json'.format(type)), 'w', encoding='utf-8') as output_file:
        json.dump(items, output_file)