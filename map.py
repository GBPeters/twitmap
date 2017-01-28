import webbrowser
from os import path

from folium import folium
from palettable.colorbrewer.sequential import Greens_9


def plotTweets(tweets, bbox):
    """
    Creates and opens a Leaflet web map with given bounding box and tweets as markers.
    Colour denotes the Tweeter's distance from home.
    :param tweets: A GeoJson dictionary containing tweets
    :param bbox: The latlon bounding box to be used as map bounds
    :return: None
    """
    print tweets
    map = folium.Map()
    breaks = [0, 1, 5, 10, 50, 100, 200, 500, 1000]
    for f in tweets["features"]:
        print f
        text = "%s: %s - Distance from home: %d km" % (f["properties"]["user"],
                                                       f["properties"]["text"],
                                                       f["properties"]["distanceFromHome"])
        dfh = f["properties"]["distanceFromHome"]
        if dfh < 0:
            c = "red"
        else:
            b = len([i for i in breaks if dfh >= i]) - 1
            c = Greens_9.hex_colors[b]
        i = folium.Icon(icon="fa-twitter", icon_color=c, prefix="fa", color="gray")
        folium.Marker(f["geometry"]["coordinates"],
                      popup=text, icon=i).add_to(map)
    map.fit_bounds([(bbox[0], bbox[1]), (bbox[2], bbox[3])])
    map.save("kaartje.html")
    fp = "file://" + path.abspath("kaartje.html")
    webbrowser.open(fp, new=2)
