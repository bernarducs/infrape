"""
manipulação das camadas geográficas
"""

import json
import dash_leaflet as dl
from infra_assets import assets

# tile layers url
basic_template = "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png"
light_template = "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png"
dark_template = "https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png"


def make_points(asset_id):
    with open(assets[asset_id]['geojson'], "r") as f:
        data = json.load(f)
    features = data["features"]
    coord = [feat['geometry']['coordinates'] for feat in features]
    texts = ["\n".join([f"{k}: {v}"
                        for k, v in feat['properties'].items()])
             for feat in features]
    point = dl.LayerGroup(
        [dl.Marker(position=[coord[1], coord[0]], title=text,
                   icon=dict(iconUrl=assets[asset_id]['url']))
         for coord, text in zip(coord, texts)], id=asset_id)
    return point


def make_geojson(asset_id):
    geojson = dl.GeoJSON(
        url=assets[asset_id]['geojson'],
        id=asset_id,
        options=dict(color=assets[asset_id]['color'],
                     weight=assets[asset_id]['weight'],
                     opacity=assets[asset_id]['opacity']),
        children=[dl.Popup(id=f"{asset_id}_popup")])
    return geojson


def get_layers():
    points = [make_points(k) for k, item in assets.items()
              if item['tipo'] == 'point']

    geojson = [make_geojson(k) for k, item in assets.items()
               if item['tipo'] != 'point']

    return geojson + points


def get_tiles():
    attribution = 'Map tiles by <a href="http://carto.com">Carto</a>, ' \
                  'under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    tiles = [
        dl.BaseLayer(
            dl.TileLayer(url=basic_template, attribution=attribution),
            name="Basic", checked=True),
        dl.BaseLayer(
            dl.TileLayer(url=light_template, attribution=attribution),
            name="Light", checked=False),
        dl.BaseLayer(
            dl.TileLayer(url=dark_template, attribution=attribution),
            name="Dark", checked=False)
    ]
    return tiles
