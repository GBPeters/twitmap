from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/testgjson")
def testgjson():
    geom = {"geometry": {"type": "Point", "coordinates": [51.56, 38.18]}, "type": "Feature", "properties": {}}
    gjson = jsonify(geom)
    return gjson

if __name__ == "__main__":
    app.run()
