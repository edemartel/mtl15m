import os
import json
import geojson
import geojson.mapping
import geojson.geometry
from shapely import geometry
from shapely import ops
import pyproj
from data import generated_path, public_path

MAX_DISTANCE = 2500

def get_real_distance(center: geometry.Point, service: geometry.Point):
    # TODO: use OpenRouteService
    return center.distance(service)

with open(os.path.join(generated_path, 'map.json'), 'r', encoding='utf-8') as input_file:
    base_map: geojson.FeatureCollection = geojson.load(input_file)

from_proj = pyproj.CRS('EPSG:4326')
to_proj = pyproj.CRS('EPSG:3857')
project = pyproj.Transformer.from_crs(
    from_proj, to_proj, always_xy=True).transform

amenities = {}
for file_name in os.listdir(os.path.join(generated_path, 'amenities')):
    type = os.path.splitext(file_name)[0]
    with open(os.path.join(generated_path, 'amenities', file_name), 'r', encoding='utf-8') as input_file:
        amenities[type] = [ops.transform(project, geometry.Point(pt)) for pt in json.load(input_file)]

for feature in base_map.features:
    center: geometry.Point = ops.transform(project, geometry.shape(feature.properties['center']))
    distances = {}
    for type, points in amenities.items():
        filtered = filter(lambda pt: center.distance(pt) <= MAX_DISTANCE, points)
        best = min(filtered, default=None, key=lambda pt: get_real_distance(center, pt))
        if best is not None:
            distances[type] = center.distance(best)
    feature.properties['distances'] = distances


with open(os.path.join(public_path, 'map.json'), 'w', encoding='utf-8') as output_file:
    geojson.dump(base_map, output_file)
