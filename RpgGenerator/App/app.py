from flask import Flask, jsonify, request, send_from_directory
from Backend.DungeonGenerator import GenerateRooms
import json
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "map.json"

@app.route("/")
def index():
    return send_from_directory("Frontend", "MapGenerator.html")

@app.route("/<path:filename>")
def frontend_file(filename):
    return send_from_directory("Frontend", filename)

@app.route('/load')
def load():
    if not file_path.exists():
        return jsonify({"error": "File does not exist"}), 404
    
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        return jsonify(data)

@app.route('/generate')
def generate():
    roomCount = request.args.get("rooms", default =5, type=int)
    dungeon  = GenerateRooms(roomNumber = roomCount)

    data={
                "map" : dungeon
    
        }
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return jsonify(
        {
            "map" : dungeon

        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)