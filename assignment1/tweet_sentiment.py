import sys
import json

def lines(fp):
    print str(len(fp.readlines()))

def build_affinity_dict(afinnfile):
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    return scores
    #print scores.items() # Print every (term, score) pair in the dictionary 

def extract_tweet_list_from_json_file(tweetfile):
    tweets = {} # initialize an empty dictionary
    tweet_list = []
    for line in tweetfile:
        tweets = json.loads(line)
        if 'text' in tweets:
            tweet_list.append(tweets['text'])

    return tweet_list

def grade_tweet(tweet, affinity_dict):
    score = 0.0
    words = tweet.split(" ")
    for word in words:
        word = word.lower()
        if word in affinity_dict:
            score += affinity_dict[word]
    
    return score

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    affinity_dict = build_affinity_dict(sent_file)
    tweet_list = extract_tweet_list_from_json_file(tweet_file)

    tweet_score = []
    for tweet in tweet_list: 
        tweet_score.append((tweet, grade_tweet(tweet, affinity_dict)))

    for tuple in tweet_score:
        print  str(tuple[1])

    #lines(sent_file)
    #lines(tweet_file)
    

if __name__ == '__main__':
    main()
