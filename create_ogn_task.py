import csv
import json

wlist = []
with open('planes.csv', newline='') as csvfile:
    planes = csv.DictReader(csvfile, delimiter=',')
    for plane in planes:
        wlist.append(plane['ID'][2::])

export_dict = {
  "tasks": [
    {
      "name": "GoZC",
      "color": "0080FF",
      "wlist": wlist,
      "legs": []
    }
  ]
}

with open('task.OGN', 'w') as f:
    json.dump(export_dict, f, indent=1)
