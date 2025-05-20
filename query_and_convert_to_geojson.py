import requests
import json
from osmtogeojson import osmtogeojson

overpass_url="https://overpass-api.de/api/interpreter"
overpass_query_file="query_edible_trees.overpassql"
geojson_result_file="deploy/fruit_trees.geojson"

with open(overpass_query_file, "r") as f:
    query_content = "".join(f.readlines())

with requests.post(url=overpass_url, data=query_content) as response:
    response_dict = json.loads(response.text)

geojson_data = osmtogeojson.process_osm_json(response_dict)

with open(geojson_result_file, "w") as f:
    json.dump(geojson_data, f, indent=2)
