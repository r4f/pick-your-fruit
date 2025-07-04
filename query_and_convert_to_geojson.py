import requests
import json
from osmtogeojson import osmtogeojson
import sys

overpass_url="https://overpass-api.de/api/interpreter"

if len(sys.argv) > 1:
    overpass_query_file=sys.argv[1]
else:
    overpass_query_file="query_edible_trees.overpassql"

geojson_result_file="deploy/fruit_trees.geojson"

with open(overpass_query_file, "r") as f:
    query_content = "".join(f.readlines())

with requests.post(url=overpass_url, data=query_content) as response:
    response_dict = json.loads(response.text)

geojson_data = osmtogeojson.process_osm_json(response_dict)

# It is easy to also display elements which are provided by a geojson file instead of bein on the OSM. This could be done with the following lines:
# additional_geojson_features_file="additional_fruit_trees.geojson"
# with open(additional_geojson_features_file, "r") as f:
#     additional_features_collection = json.load(f)
# geojson_data["features"].extend(additional_features_collection["features"])

with open(geojson_result_file, "w") as f:
    json.dump(geojson_data, f, indent=2)
