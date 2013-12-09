from flask import Flask, jsonify
import pyelasticsearch as es

from twit import config



app = Flask("twit")
app.debug = True
cfg = config.get_config()
client = es.ElasticSearch(urls=[cfg.get("ES_URL", "http://localhost:9200")])


def build_query(lat, lon):
    return {
        "query": {
            "filtered": {
                "query": {"match_all": {}},
                "filter": {
                    "geo_distance": {
                        "distance": "50km",
                        "tweet.location": {
                            "lon": lon,
                            "lat": lat,
                        }
                    }
                }
            }
        },
        "sort": [
            {"timestamp": {"order": "desc"}},
        ],
    }


@app.route("/search/lonlat/<lon>+<lat>")
def search(lat, lon):
    lat, lon = float(lat), float(lon)
    query = build_query(lat, lon)
    results = [
        hit["_source"] for hit in
        client.search(index="twit", doc_type="tweet", query=query)["hits"]["hits"]]
    return jsonify({"tweets": results})
