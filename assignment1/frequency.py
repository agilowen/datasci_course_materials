import sys
import json

def lines(fp):
    print str(len(fp.readlines()))

def extract_tweet_list_from_json_file(tweetfile):
    tweets = {} # initialize an empty dictionary
    tweet_list = []
    for line in tweetfile:
        tweets = json.loads(line)
        if 'text' in tweets:
            tweet_list.append(tweets['text'])

    return tweet_list


def main():
    tweet_file = open(sys.argv[1])
    
    tweet_list = extract_tweet_list_from_json_file(tweet_file)

    term_occurence_dict = {}
    for tweet in tweet_list:
        words = tweet.split(" ")
        for word in words:
            if word in term_occurence_dict:
                term_occurence_dict[word] += 1
            else:
                term_occurence_dict[word] = 1 

    sum_occurences = 0
    for key in term_occurence_dict:
        sum_occurences += term_occurence_dict[key]

    for key in term_occurence_dict:
        frequency = 0
        frequency = term_occurence_dict[key] * 1.0 / sum_occurences
        print key.encode("utf-8").replace("\n"," ") + " %0.4f" % frequency
    


if __name__ == '__main__':
    main()
