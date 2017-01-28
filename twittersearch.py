import json

from geopy import Nominatim
from haversine import haversine
from twython import Twython

APP_KEY = 'KvvFEg9TcDODoLr5YSSouVJMv'
APP_SECRET = 'UQTiJdbS0HC3MBA4d4YyeZaiY881pbeRRGtKkoqbgmtzb29mKU'


def getTweets(coords, radius, q=""):
    """
    Basic location search function.
    :param coords: latlon tuple
    :param radius: radius in km
    :param q: query text
    :return: dictionary with results
    """
    token = Twython(APP_KEY, APP_SECRET, oauth_version=2).obtain_access_token()
    twitter = Twython(APP_KEY, access_token=token)
    gc = "%f,%f,%fkm" % (coords[0], coords[1], radius)
    result = twitter.search(q=q, geocode=gc, count=100, result_type="recent")
    return result


def geocode(name):
    """
    Wrapper around geopy.geocode
    :param name: The name to geocode
    :return: latlon tuple, or None if geocode failed.
    """
    try:
        locator = Nominatim()
        location = locator.geocode(name, exactly_one=True)
        if location is not None:
            return (location.latitude, location.longitude)
    except Exception, e:
        print "Geocode error:", e.message


def calculateDistance(latlon1, latlon2):
    """
    Calculates (Haversine) great circle distance
    :param latlon1: latlon tuple
    :param latlon2: latlon tuple
    :return: distance in km, or None if invalid arguments were passed.
    """
    if latlon1 is not None and latlon2 is not None:
        return haversine(latlon1, latlon2)
    else:
        return -9999


def processTweets(tweets):
    """
    Processes a Json dictionary of tweets, and prepares it for plotting.
    :param tweets: The Json dictionary of tweets
    :return: a GeoJson string to be plotted
    """
    dic = {"type": "FeatureCollection",
           "features": []}
    for tweet in tweets["statuses"]:
        if "coordinates" in tweet and tweet["coordinates"] is not None:
            f = createGeoJSONDict(tweet)
            dic["features"].append(f)
    return json.dumps(dic)


def createGeoJSONDict(tweet):
    """
    Create a JSON dictionary from a tweet
    :param tweet: A tweet in a dictionary
    :return: A GeoJSON Feature dictionary
    """
    tid = tweet["id"]
    user = tweet["user"]["name"]
    text = tweet["text"]
    coordinates = (tweet["coordinates"]["coordinates"][1], tweet["coordinates"]["coordinates"][0])
    geom = {"type": "Point", "coordinates": coordinates}
    userloc = tweet["user"]["location"]
    latlon1 = tuple(geom["coordinates"])
    latlon2 = geocode(userloc)
    distancefromhome = calculateDistance(latlon1, latlon2)
    if latlon2 is not None:
        userlocgeom = {"type": "Point", "coordinates": list(latlon2)}
    else:
        userlocgeom = None
    dic = {"type:": "Feature",
           "geometry": geom,
           "properties": {
               "tid": tid,
               "user": user,
               "text": text,
               "userloc": userloc,
               "userlocgeom": userlocgeom,
               "distanceFromHome": distancefromhome
           }}
    return dic


if __name__ == "__main__":
    r = getTweets((52.38, 4.9), 10)
    gjson = processTweets(r)
    print gjson
