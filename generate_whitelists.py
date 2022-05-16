import csv
import json
from dataclasses import dataclass

@dataclass
class Plane:
    plane_type: str
    competition_id: str
    registration: str
    flarm_id: str

wlist = []
planes = []
with open('planes.csv', newline='') as csvfile:
    for plane in csv.DictReader(csvfile, delimiter=','):
        planes.append(Plane(plane['TYPE'], plane['CN'], plane['CALL'], plane['ID'][2::]))
        wlist.append(plane['ID'][2::])


def serialize_for_glide_and_seek(plane: Plane) -> dict:
    return {
        "cn": plane.competition_id,
        "glider": plane.plane_type,
        "flarm": [plane.flarm_id],
        "name": plane.registration,  # TODO: owner? necessarily unique?
    }

with open('glide_and_seek.json', 'w') as f:
    serialized = []
    for plane in planes:
        serialized.append(serialize_for_glide_and_seek(plane))
    json.dump(serialized, f)




# export_dict = {
#   "tasks": [
#     {
#       "name": "GoZC",
#       "color": "0080FF",
#       "wlist": wlist,
#       "legs": []
#     }
#   ]
# }

# with open('task.OGN', 'w') as f:
#     json.dump(export_dict, f, indent=1)
