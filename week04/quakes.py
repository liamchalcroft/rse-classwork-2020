"""A script to find the biggest earthquake in an online dataset."""

# At the top of the file, import any libraries you will use.
import json
import requests
from IPython.display import Image

# If you want, you can define some functions to help organise your code.
def search_for_largest(quakes):
    largest_so_far = quakes[0]
    for quake in quakes:
        if quake['properties']['mag'] > largest_so_far['properties']['mag']:
            largest_so_far = quake
    return largest_so_far

def request_map_at(lat, long, satellite=True,
                   zoom=10, size=(400, 400)):
    base = "https://static-maps.yandex.ru/1.x/?"

    params = dict(
        z=zoom,
        size="{},{}".format(size[0], size[1]),
        ll="{},{}".format(long, lat),
        l="sat" if satellite else "map",
        lang="en_US"
    )

    return requests.get(base, params=params)

# When you run the file, it should print out the location and magnitude
# of the biggest earthquake.
# You can run the file with `python quakes.py` from this directory.
if __name__ == "__main__":
    # ...do things here to find the results...

    # load quake info file

    quakes = requests.get("http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
                        params={
                        'starttime': "2000-01-01",
                        "maxlatitude": "58.723",
                        "minlatitude": "50.008",
                        "maxlongitude": "1.67",
                        "minlongitude": "-9.756",
                        "minmagnitude": "1",
                        "endtime": "2018-10-11",
                        "orderby": "time-asc"}
                        )
    
    requests_json = json.loads(quakes.text)

    quakes = requests_json['features']

    # search for largest magnitude feature

    largest_so_far = search_for_largest(quakes)

    lat = largest_so_far['coordinates'][0]
    lon = largest_so_far['coordinates'][1]
    alt = largest_so_far['coordinates'][2]

    # plot map of earthquake

    map_png = request_map_at(lat, lon, zoom=10, satellite=False)

    Image(map_png.content)

    # The lines below assume that the results are stored in variables
    # named max_magnitude and coords, but you can change that.
    print(f"The maximum magnitude is {max_magnitude} "
          f"and it occured at coordinates {coords}.")
