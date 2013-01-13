import twitter, pickle
from itertools import groupby
class post:
    def __init__(self,content,reposts,likes):
        """general post class"""
        self.content = content
        self.likes = likes
        self.reposts = reposts
class connection:
    """to be used for every connection between the bot and the service"""
    def __init__(self,conkey,consec,actoke,acsecr,fileName):
        """sets up api to connect to twitter
        Takes consumer key, consumer secret, access key, acess secret, save file name in that order"""
        self.fileName = fileName
        self.api = twitter.Api(consumer_key=conkey,consumer_secret=consec,access_token_key=actoke,access_token_secret=acsecr)
    def update_posts(self):
        """updates the save file of all posts. got get the tweets, use get_posts"""
        self.save_posts(self.get_posts())
    def get_old_posts(self):
        """get saved posts from the file. faster than getting new posts, so if it's not critical you have the latest info, you can use this"""
        loadFile = file(self.fileName)
        oldTweets = pickle.load(loadFile)
        loadFile.close()
        return oldTweets
    def get_new_posts(self):
        """gets all new posts from twitter. Usefull for measuring changes"""
        return self.api.GetFriendsTimeline(count=100)
    def save_posts(self,tweets):
        """used internaly. Pas it a list of tweets to overwite the save with those tweets"""
        loadFile = file(self.fileName,"w")
        oldtweets = pickle.dump(tweets,loadFile)
        loadFile.close()
    def get_posts(self):
        """gets all tweets, treurns them as post classes"""
        oldTweets = self.get_old_posts()
        newTweets = []
        for i in self.get_new_posts():
            newTweets.append(apitopost(i))
        for i in newTweets:
            if i not in oldTweets:
                oldTweets.append(i)
        return oldTweets
    def make_post(self,tweetstring):
        """makes a new post. Pass it a string. simple """
        tweetstring = tweetstring[:140]
        self.api.PostUpdates(tweetstring)
def apitopost(tweet):
    return post(tweet.text,tweet.retweet_count,tweet.favorited)
#output.make_tweet('toast')
