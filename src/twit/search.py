from flask import Flask, jsonify
import pyelasticsearch as es


app = Flask("twit")
app.debug = True
client = es.ElasticSearch(urls=["http://localhost:49167"])


def build_query(lat, lon):
    return {
        "query": {
            "filtered": {
                "query": {"match_all": {}},
                "filter": {
                    "geo_distance": {
                        "distance": "1km",
                        "tweet.location": {
                            "lon": lon,
                            "lat": lat,
                        }}}}}}

@app.route("/search/lonlat/<lon>+<lat>")
def search(lat, lon):
    lat, lon = float(lat), float(lon)
    query = build_query(lat, lon)
    results = [
        hit["_source"] for hit in
        client.search(index="twit", doc_type="tweet", query=query)["hits"]["hits"]]
    return jsonify({"tweets": results})
