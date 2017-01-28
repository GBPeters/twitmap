#imports
from threading import Thread

from twython import TwythonStreamer

from map import plotTweets
from twittersearch import createGeoJSONDict

APP_KEY = 'nNJW0Htrw5hzFYoKljPUlKBzk'
APP_SECRET = '9AoAc8YwguVy6YLHEAcum2Ho1nlRyrK5fRsnOkgwNV1Zd8AbdT'
TOKEN = '3247956964-ov5UMweNO0l1ayQVcgc2HxkJzCu7UUbAT3TnGA9'
TOKEN_SECRET = 'oO5ZBP9yp9Klg3isi3OXEC1O7ymgv0TyLMjdkxRPYHTox'

BBOX = (-74, 40, -73, 41)
BBOX_LATLON = (BBOX[1], BBOX[0], BBOX[3], BBOX[2])


# Class to process JSON data comming from the twitter stream API. Extract relevant fields
class TwitterStreamer(TwythonStreamer):
    """
    Customised TwythonStreamer
    """

    def __init__(self, bbox, maxTweets=0, callbackFinish=None):
        """
        Public constructor
        :param bbox: lonlat boundingbox to filter on.
        :param maxTweets: Number of geolocated tweets to harvest. If set to 0, harvesting will continue indefinitely.
        :param callbackFinish: callback function to call when number of tweets is reached. If set to None, internal
        plot method will be called.
        """
        self.bbox = bbox
        sbbox = "%s,%s,%s,%s" % bbox
        self.maxTweets = maxTweets
        self.tweets = {"type": "FeatureCollection",
                       "features": []}
        self.callbackFinish = callbackFinish
        TwythonStreamer.__init__(self, APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
        self.statuses.filter(locations=sbbox)



    def on_success(self, data):
        print data
        if "coordinates" in data and data["coordinates"] is not None:
            f = createGeoJSONDict(data)
            self.tweets["features"].append(f)
        if len(self.tweets["features"]) >= self.maxTweets and self.maxTweets > 0:
            self.disconnect()
            if self.callbackFinish is None:
                self._finished(self)
            else:
                self.callbackFinish(self)


    def on_error(self, status_code, data):
        print "Error: " + str(status_code)
        # self.disconnect

    def _finished(self, streamer):
        """
        Plot tweets when finished
        :param streamer: The streamer object
        :return: None
        """
        bboxlatlon = (self.bbox[1], self.bbox[0], self.bbox[3], self.bbox[2])
        plotTweets(streamer.tweets, bboxlatlon)


class HarvestThread(Thread):
    """
    Multithreading wrapper around harvest class
    """

    def __init__(self, bbox, ntweets, callback):
        """
        Public constructor
        :param bbox: The bounding box to filter on
        :param ntweets: The number of tweets to harvest
        :param callback: The callback when the thread finishes. Note, this is not the same as the TwitterStreamer callback.
        For now, only default callback can be used in the TwitterStreamer class.
        """
        self.bbox = bbox
        self.callback = callback
        self.ntweets = ntweets
        Thread.__init__(self)

    def run(self):
        main(self.bbox, self.ntweets)
        self.callback()


def main(bbox, ntweets):
    """
    main function
    :param ntweets: The number of tweets to harvest
    :param bbox: The bounding box to filter on.
    :return:
    """
    try:
        stream = TwitterStreamer(bbox, maxTweets=ntweets)
    except ValueError, e:
        print 'Error during setup:', e.message

if __name__ == '__main__':
    main(BBOX)
