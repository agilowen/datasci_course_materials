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

def build_text_dict(tweetfile):
    tweets = {} # initialize an empty dictionary
    tweets = json.load(tweetfile)
    return tweets
    
def extract_tweet_list(tweet_dict):
    tweet_list = []
    results_list = []
    #Get the results dictionary from the dictionary
    for key in tweet_dict:
        if key == "results":
            results_list = tweet_dict[key]

    #Extract the individual tweets dictionaries, then their texts
    for full_tweet_dict in results_list:
        for key in full_tweet_dict:
            if key == "text":
                tweet_list.append(full_tweet_dict[key]) 

    return tweet_list

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

def find_new_terms(tweet, affinity_dict):
    new_terms = []
    words = tweet.split(" ")
    for word in words:
        word = word.lower()
        if word not in affinity_dict:
            new_terms.append(word)

    return new_terms


def count_pos_or_neg_words(tweet, affinity_dict, pos):
    neg_words = 0
    pos_words = 0
    words = tweet.split(" ")
    for word in words:
        word = word.lower()
        if word in affinity_dict:
            if affinity_dict[word] > 0:
                pos_words+=1
            if affinity_dict[word] < 0:
                neg_words+=1

    if pos is True:
        return pos_words
    else:
        return neg_words

#Uses total positve words and total negative words across ALL tweets
def calculate_new_term_score(tot_pos_words, tot_neg_words):
    if tot_pos_words == 0:
        tot_pos_words = 1

    if tot_neg_words == 0:
        tot_neg_words = 1

    score = 0.0
    score = tot_pos_words * 1.0 / tot_neg_words

    return score

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    affinity_dict = build_affinity_dict(sent_file)
    tweet_list = extract_tweet_list_from_json_file(tweet_file)
    #tweet_dict = build_text_dict(tweet_file)
    #tweet_list = extract_tweet_list(tweet_dict)

    #{term, [pos frequency, neg frequency]}
    new_terms_pos_neg_dict = {}
    for tweet in tweet_list: 
        new_terms_list = find_new_terms(tweet, affinity_dict)
        num_pos_words = count_pos_or_neg_words(tweet, affinity_dict, True)
        num_neg_words = count_pos_or_neg_words(tweet, affinity_dict, False)
        
        for new_term in new_terms_list:
            if new_term in new_terms_pos_neg_dict:
                new_terms_pos_neg_dict[new_term][0]+=num_pos_words
                new_terms_pos_neg_dict[new_term][1]+=num_neg_words
            else: 
                new_terms_pos_neg_dict[new_term] = [num_pos_words, num_neg_words]

    #print new_terms_pos_neg_dict.items()

    for new_term in new_terms_pos_neg_dict:
        score = calculate_new_term_score(new_terms_pos_neg_dict[new_term][0], new_terms_pos_neg_dict[new_term][1])
        print new_term + " %0.4f" % score

if __name__ == '__main__':
    main()
