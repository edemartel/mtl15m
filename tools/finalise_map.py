import os
import json

import urllib
import geojson
import geojson.mapping
import geojson.geometry
from shapely import geometry
from shapely import ops
import pyproj
import math
from data import generated_path, public_path


MAX_DISTANCE = 2500

from_proj = pyproj.CRS('EPSG:4326')
to_proj = pyproj.CRS('EPSG:3857')
project = pyproj.Transformer.from_crs(
    from_proj, to_proj, always_xy=True).transform


class MapPoint:
    point_in_degrees: geometry.Point
    point_in_metres: geometry.Point

    def __init__(self, pt: geometry.Point):
        self.point_in_degrees = pt
        self.point_in_metres = ops.transform(project, pt)


def get_real_distance(center: MapPoint, service: MapPoint):
    request = urllib.request.Request(
        f'http://localhost:8082/ors/v2/directions/foot-walking?start={center.point_in_degrees.x},{center.point_in_degrees.y}&end={service.point_in_degrees.x},{service.point_in_degrees.y}')
    request.add_header('content-type', 'application/json')
    try:
        with urllib.request.urlopen(request) as rawResponse:
            response = json.load(rawResponse)
            summary = response['features'][0]['properties']['summary']
            if 'distance' not in summary:
                return math.inf
            else:
                return summary['distance']
    except urllib.error.HTTPError as e:
        return math.inf

    # return center.point_in_metres.distance(service.point_in_metres)


with open(os.path.join(generated_path, 'map.json'), 'r', encoding='utf-8') as input_file:
    base_map: geojson.FeatureCollection = geojson.load(input_file)

amenities = {}
for file_name in os.listdir(os.path.join(generated_path, 'amenities')):
    type = os.path.splitext(file_name)[0]
    with open(os.path.join(generated_path, 'amenities', file_name), 'r', encoding='utf-8') as input_file:
        amenities[type] = [MapPoint(geometry.Point(pt))
                           for pt in json.load(input_file)]

for feature in base_map.features:
    center = MapPoint(geometry.shape(feature.properties['center']))
    distances = {}
    for type, points in amenities.items():
        best = (None, math.inf)
        for pt in points:
            if center.point_in_metres.distance(pt.point_in_metres) > MAX_DISTANCE:
                continue
            dist = get_real_distance(center, pt)
            if dist < best[1]:
                best = (pt, dist)
        if best[0] is not None:
            distances[type] = {
                'pt': geojson.mapping.to_mapping(best[0].point_in_degrees),
                'dist': best[1]
            }
    feature.properties['distances'] = distances


with open(os.path.join(public_path, 'map.json'), 'w', encoding='utf-8') as output_file:
    geojson.dump(base_map, output_file)
