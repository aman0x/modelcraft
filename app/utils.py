import json

def walls_to_json(walls):
    walls_data = [{'points': wall[:, 0, :].tolist()} for wall in walls]
    return json.dumps(walls_data)

