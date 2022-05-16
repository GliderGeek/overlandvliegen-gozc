
"""
Generate whitelists from planes.csv to filter Gooise airplanes on various tracking sites.
Generates files next to script:
- live.glidernet (glidernet.OGN)
- glidertracker.de (glidertracker.csv)
- glideandseek.com (glideandseek.json)
"""

import csv
import json
from dataclasses import dataclass


@dataclass
class Plane:
    plane_type: str
    competition_id: str
    registration: str
    flarm_id: str


planes = []
with open('planes.csv', newline='') as csvfile:
    for plane in csv.DictReader(csvfile, delimiter=','):
        planes.append(Plane(plane['TYPE'], plane['CN'], plane['CALL'], plane['ID'][2::]))


def serialize_glidertracker(plane: Plane) -> dict:
    return {
        "ID": f"06{plane.flarm_id}",
        "CALL": plane.registration,
        "CN": plane.competition_id,
        "TYPE": plane.plane_type,
    }


def serialize_glideandseek(plane: Plane) -> dict:
    return {
        "cn": plane.competition_id,
        "glider": plane.plane_type,
        "flarm": [plane.flarm_id],
        "name": plane.registration,  # TODO: owner? necessarily unique?
    }


def write_glidernet(planes, f):
    wlist = [plane.flarm_id for plane in planes]
    export_dict = {
        "tasks": [{
            "name": "GoZC",
            "color": "0080FF",
            "wlist": wlist,
            "legs": []
        }]
    }

    json.dump(export_dict, f, indent=1)


with open('glideandseek.json', 'w') as f:
    serialized = []
    for plane in planes:
        serialized.append(serialize_glideandseek(plane))
    json.dump(serialized, f)

with open('glidertracker.csv', 'w', newline='') as f:
    serialized_planes = [serialize_glidertracker(plane) for plane in planes]
    writer = csv.DictWriter(f, serialized_planes[0].keys())
    writer.writeheader()
    writer.writerows(serialized_planes)

with open('glidernet.OGN', 'w') as f:
    write_glidernet(planes, f)
