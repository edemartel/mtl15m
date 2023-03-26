import os
import geojson
import geojson.mapping
import geojson.geometry
import pyproj
from shapely import geometry
from shapely import ops
from data import source_path, generated_path
import shapefile
import csv
import zipfile
import io

MIN_POPULATION = 1

population = {}
with zipfile.ZipFile(os.path.join(source_path, 'map', '98100015-fra.zip')) as zip:
    with io.TextIOWrapper(zip.open('98100015.csv'), encoding='utf-8', newline='') as input_file:
        reader = csv.reader(input_file, delimiter=';')
        next(reader, None)
        for row in reader:
            if len(row) >= 5 and len(row[2]) == 17 and row[2][9:13] == '2466' and row[4] != '..':
                pop = int(row[4])
                if pop >= MIN_POPULATION:
                    population[row[2]] = pop

with open(os.path.join(source_path, 'map', 'limites-terrestres.geojson'), 'r', encoding='utf-8') as input_file:
    ground_boundaries = geojson.load(input_file)
    ground_boundaries = ops.unary_union([geometry.shape(f.geometry) for f in ground_boundaries.features])

from_proj = pyproj.CRS('EPSG:3347')
to_proj = pyproj.CRS('EPSG:4326')
project = pyproj.Transformer.from_crs(
    from_proj, to_proj, always_xy=True).transform

features = []
with shapefile.Reader(os.path.join(source_path, 'map', 'lad_000a21a_f.zip')) as reader:
    for shape_rec in reader.iterShapeRecords():
        pop = population.get(shape_rec.record.IDUGD)
        if pop is None:
            continue

        shape = geometry.shape(shape_rec.shape.__geo_interface__)
        shape = ops.transform(project, shape)
        shape = ground_boundaries.intersection(shape)

        center_point = geojson.mapping.to_mapping(shape.centroid)

        mapped = geojson.mapping.to_mapping(shape)
        properties = {
            'population': pop,
            'area': float(shape_rec.record.SUPTERRE),
            'center': center_point
        }

        features.append(geojson.Feature(shape_rec.record.ADIDU, mapped, properties))

with open(os.path.join(generated_path, 'map.json'), 'w', encoding='utf-8') as output_file:
    feature_collection = geojson.FeatureCollection(features)
    geojson.dump(feature_collection, output_file)
