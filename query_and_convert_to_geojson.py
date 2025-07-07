from typing import Collection
import requests
import json
from osmtogeojson import osmtogeojson
import sys
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON as SPARQLWrapper_JSON

def get_wikipedia_articles(wikidata_ids: Collection[str]):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(SPARQLWrapper_JSON)

    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint
    sparql.setQuery(f"""
    SELECT DISTINCT ?item ?lang ?article WHERE {{
      VALUES ?item {{
        {"\n".join(f"wd:{wd_id}" for wd_id in wikidata_ids)}
      }}

      ?article schema:about ?item . hint:Prior hint:runFirst true.
      ?article schema:inLanguage ?lang ;
        schema:name ?name ;
        schema:isPartOf [ wikibase:wikiGroup "wikipedia" ] .
      FILTER(?lang in ('en', 'de')) .
    }}
        """
    )

    result_all_responses = {}
    try:
        ret = sparql.queryAndConvert()
        for r in ret["results"]["bindings"]:
            wd_id = r["item"]["value"].removeprefix("http://www.wikidata.org/entity/")
            lang = r["lang"]["value"]
            result_all_responses.setdefault(wd_id, {})
            result_all_responses[wd_id][lang] = r["article"]["value"]
    except Exception as e:
        raise

    results = {k: v.get("de", v.get("en")) for k, v in result_all_responses.items()}

    return results


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

wikidata_ids = set()

#gather all wikidata links
for feature in response_dict["elements"]:
    for key, value in feature["tags"].items():
        if key.endswith(":wikidata"):
            wikidata_ids.add(value)

print(wikidata_ids)

try:
    linking = get_wikipedia_articles(wikidata_ids)
    print(linking)
except Exception:
    pass

for feature in response_dict["elements"]:
    tags = feature["tags"]
    wikidata_id = tags.get(
        "taxon:wikidata",
        tags.get(
            "species:wikidata",
            tags.get(
                "genus:wikidata",
                None
            )
        )
    )
    if wikidata_id is not None:
        wikipedia_url = linking.get(wikidata_id)
        if wikipedia_url is not None:
            tags["wikipedia_url"] = wikipedia_url

geojson_data = osmtogeojson.process_osm_json(response_dict)

# It is easy to also display elements which are provided by a geojson file instead of bein on the OSM. This could be done with the following lines:
# additional_geojson_features_file="additional_fruit_trees.geojson"
# with open(additional_geojson_features_file, "r") as f:
#     additional_features_collection = json.load(f)
# geojson_data["features"].extend(additional_features_collection["features"])

with open(geojson_result_file, "w") as f:
    json.dump(geojson_data, f, indent=2)
