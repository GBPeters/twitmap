#imports
from twython import TwythonStreamer
from datetime import datetime
import csv

# get access to the twitter API
APP_KEY = 'nNJW0Htrw5hzFYoKljPUlKBzk'
APP_SECRET = '9AoAc8YwguVy6YLHEAcum2Ho1nlRyrK5fRsnOkgwNV1Zd8AbdT'
TOKEN = '3247956964-ov5UMweNO0l1ayQVcgc2HxkJzCu7UUbAT3TnGA9'
TOKEN_SECRET = 'oO5ZBP9yp9Klg3isi3OXEC1O7ymgv0TyLMjdkxRPYHTox'


# Class to process JSON data comming from the twitter stream API. Extract relevant fields
class TwitterStream (TwythonStreamer):
    def on_success(self, data):
        tweet_lat = 0.0
        tweet_lon = 0.0
        tweet_name = ""
        tweet_text = ""
        tweet_datetime = ""

        if 'id' in data:
            tweet_id = data['id']
        if 'text' in data:
            tweet_text = data['text'].encode('utf-8').replace("'", "''").replace(';', '')
        if 'coordinates' in data:
            geo = data['coordinates']
            if geo != None:
                latlon = geo['coordinates']
                tweet_lon = latlon[0]
                tweet_lat = latlon[1]
        if 'created_at' in data:
            dt = data['created_at']
            tweet_datetime = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
        if 'user' in data:
            users = data['user']
            tweet_name = users['screen_name']
        if tweet_lat != 0:
            # some elementary output to console
            string_to_write = "date and time = {}, lat = {}, lon = {}, name = {}, text= {}".format(tweet_datetime,
                                                                                                   tweet_lat, tweet_lon,
                                                                                                   tweet_name,
                                                                                                   tweet_text)
            print string_to_write


    def on_error(self, status_code, data):
        print str(status_code)
        # self.disconnect

##main procedure
def main(hashtag, Bbox):
    try:
        stream = TwitterStream(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
        print 'Connecting to twitter: will take a minute'
    except ValueError:
        print 'OOPS! that hurts, something went wrong while making connection with Twitter: ' + str(ValueError)
    # global target


    # Filter based on bounding box see twitter api documentation for more info
    try:
        stream.statuses.filter(track=hashtag, locations=Bbox)
    except ValueError:
        print 'OOPS! that hurts, something went wrong while getting the stream from Twitter: ' + str(ValueError)

if __name__ == '__main__':
main('#Amsterdam', '3.00,50.00,7.35,53.65')
