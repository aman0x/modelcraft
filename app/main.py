from flask import Flask, render_template
from wall_detection import detect_walls
from utils import walls_to_json

app = Flask(__name__)

@app.route('/')
def index():
    walls = detect_walls('floorplans/floorplan.png')
    walls_json = walls_to_json(walls)
    print(walls_json)  # Debugging
    return render_template('index.html', walls_json=walls_json)

if __name__ == '__main__':
    app.run(debug=True)
