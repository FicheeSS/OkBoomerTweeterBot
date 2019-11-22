import tweepy
import csv
from user import CONSUMER_KEY , CONSUMER_SECRET , ACCES_TOKEN , ACCES_TOKEN_SECRET
import time

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCES_TOKEN, ACCES_TOKEN_SECRET)


api = tweepy.API(auth)
DayTweet = [[],[]]

def getTweetFromMP():
    IsMessagesLeft = True
    while IsMessagesLeft  :
        messages = api.list_direct_messages(100)
        print(messages)
        if messages != "":
            for msg in messages :
                cm = api.get_direct_message(msg)
                if IfTweetValid(msg) and cm["in_reply_to_status_id"] == "" :
                    Exist = False
                    for line in DayTweet[0]:
                        if msg == line:
                            Exist = True
                            l = line
                            break
                if Exist :
                    DayTweet[1][l] += 1
                else:    
                    DayTweet[0].append(cm)
                    DayTweet[1].append(1)
                api.destroy_direct_message(cm)                  
        else :
            IsMessagesLeft = False
        
def SendBestTweet():
    bests = [[0,""],[0,""],[0,""]]
    totalSuggestedTweets = 0 
    for n in DayTweet[1]:
        if n > bests[0][0] :
            bests[2][0] = bests[1][0]
            bests[1][0] = bests[0][0]
            bests[2][1] = bests[1][1]
            bests[1][1] = bests[0][1]
            bests[0][0] = n
            bests[0][1] = DayTweet[0][n]
        elif n > bests[1][0] :
            bests[2][0] = bests[1][0]
            bests[2][1] = bests[1][1]
            bests[1][0] = n
            bests[1][1] = DayTweet[0][n]
        elif  n > bests[2][0] :
            bests[2][0] = n
            bests[2][1] = DayTweet[0][n]
        totalSuggestedTweets += n     
    api.update_status(tweetMsg(bests))
    for b in bests[0]:
        api.update_status("Ok boomer",in_reply_to_status_id=b["id"])            

def tweetMsg(bests):
    return "Les trois tweet de boomer sélectionés sont \n 1 - "+bests[0][0] +" : " + bests[0][1] + "\n 2 - " +bests[1][0] +" : " + bests[1][1] + "\n 3 - "+bests[2][0] +" : " + bests[2][1]   

def IfTweetValid(msg):
    return True
    