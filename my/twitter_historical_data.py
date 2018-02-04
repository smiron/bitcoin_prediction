import tweepy
import time
import json
import csv
import sys
import traceback

def main():
    
    # set twitter api credentials
    consumer_key= 'bgnlPZMTy7kwpwUdU8t1PBxxD'
    consumer_secret= 'AJ6QI66gI1TGb6vmQYF2dMMRiPdbG5OuUAZB7wJKTWq2IDxUKS'
    access_token='353354840-8iXpn2Mha8pZaBkAEgqgIFl5q2q25hFDN6J9AzaM'
    access_token_secret='ZcLSQCLjgJLXEoqZt8uUlfVxOcakvZpYAmCS9LBVFTw4N'

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)

    searchTerms = ['bitcoin OR btc OR xbt OR satoshi OR xrp OR ripple']

    tweets = twitter_api.search(q=searchTerms, count=100)
    fetchData = processTweets(tweets)

    while fetchData:
        time.sleep(2)
        try:
            tweets = twitter_api.search(q=searchTerms, count=100, max_id = tweets.max_id, lang='en')
            fetchData = processTweets(tweets)
        except:        
            exc_type, exc_value, exc_traceback = sys.exc_info()
            with open('errors.csv', mode='a') as file:           
                traceback.print_exc(file=file)
                file.write(('-'*100)+'\n\n')

def processTweets(tweets):

    if tweets.count > 0:
        print(tweets.max_id, ' - ', tweets.count, ' - ', tweets[0].created_at)
        
        with open("twitter_historic.csv", mode='a', encoding='utf-8', newline='') as file:

            fieldnames = ['id', 'created_at', 'lang', 'text']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for t in tweets:
                #file.write('{0},{1},{2},{3}\n'.format(t.id, t.created_at, t.lang, t.text.re))
                writer.writerow({'id': t.id, 'created_at': t.created_at, 'lang': t.lang, 'text': t.text.replace('\n', '').replace('\r', '').replace('\t', '')})
            file.flush()

        return True
    
    return False

main()