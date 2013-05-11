import sys
import json
import operator

def find_occurence_of_hashes(tweetfile):
    tweets = {} # initialize an empty dictionary
    hash_occurence = {}
    for line in tweetfile:
        tweets = json.loads(line)
        if 'entities' in tweets:
            if 'hashtags' in tweets['entities']:
                for hash_dict in tweets['entities']['hashtags']:
                    tag = hash_dict['text']
                    if tag in hash_occurence:
                        hash_occurence[tag] += 1
                    else:
                        hash_occurence[tag] = 1

    return hash_occurence

def main():
    tweet_file = open(sys.argv[1])
    
    hash_occurence = find_occurence_of_hashes(tweet_file)

    sorted_hash = sorted(hash_occurence.iteritems(), key=operator.itemgetter(1), reverse=True)

    for i in range(0,10):
        print sorted_hash[i][0] + " %.1f" % sorted_hash[i][1]

if __name__ == '__main__':
    main()
