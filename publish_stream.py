from datetime import datetime
import time
from twython import TwythonStreamer
from fluent import sender
from fluent import event
import os
# for local fluent
sender.setup('twitter')

class MyStreamer(TwythonStreamer):

    def save_tweet(self, tweet, tag):
        event_contents = {
                'tweet_id': tweet['id_str'].encode('utf-8'),
                'username': tweet['user']['screen_name'].encode('utf-8'),
                'userid' : tweet['user']['id_str'].encode('utf-8'),
                'lang' : tweet['lang'].encode('utf-8'),
                'text': tweet['text'].encode('utf-8')
                }
        if 'in_reply_to_status_id_str' in tweet:
            event_contents['reply_to_status'] = tweet['in_reply_to_status_id_str']
        if 'in_reply_to_user_id_str' in tweet:
            event_contents['reply_to_userid'] = tweet['in_reply_to_user_id_str']
        tweet_time = time.mktime(datetime.strptime(tweet['created_at'],
                                                   '%a %b %d %H:%M:%S +0000 %Y').timetuple())
        event.Event(tag,
                    event_contents,
                    time=tweet_time)

    def on_success(self, data):
        if 'friends' in data:
            print "got friends list, ignoring"
        elif 'event' in data:
            if data['event']=="favorite":
                tweet = data['target_object']
                print "favoriting tweet: "+tweet['text'].encode('utf-8')
                self.save_tweet(tweet, "scsibug.favorites")
        elif 'user' in data:
            self.save_tweet(data, "scsibug.timeline")
        else:
            print "got an unknown event:"
            print data
    def on_error(self, status_code, data):
        print status_code

stream = MyStreamer(os.environ.get('APP_KEY'),
                    os.environ.get('APP_SECRET'),
                    os.environ.get('OAUTH_TOKEN'),
                    os.environ.get('OAUTH_TOKEN_SECRET'))

stream.user(replies='all')
# For just our user and those we follow, use:
#stream.user()
