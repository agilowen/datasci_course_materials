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

def extract_tweet_list_and_state_from_json_file(tweetfile, states):
    tweets = {} # initialize an empty dictionary
    tweet_state_list = []
    for line in tweetfile:
        state_match = False
        tweets = json.loads(line)
        
        if 'user' in tweets:
            if 'location' in tweets['user']:
                location_words = tweets['user']['location'].split(" ")
                for word in location_words:
                    if word.lower() in states:
                        state = word.lower() 
                        #special handling for north/south dakota/carolina
                        if (state == 'dakota' or state == 'carolina'):
                            for word in location_words:
                                if word.lower() == 'north':
                                    state = state
                                    state_match = True
                                    break
                                if word.lower() == 'south':
                                    state = 'south'+state
                                    state_match = True
                                    break
                            if state_match is False:
                                #can't tell if north or south dakota/carolina
                                break

                        #special handling for west virginia and virginia
                        if (state == 'virginia'):
                            for word in location_words:
                                if word.lower() == 'west':
                                    state = 'westvirginia'
                                    break

                        #special handling for new mexico / new york
                        if (state == 'mexico' or state == 'york'):
                            for word in location_words:
                                if word.lower() == 'new':
                                    state_match = True
                                    break

                            if state_match is False:
                                #this is mexico, not new mexcio (or not new york)
                                break
                        
                        state_match = True
                        #print "Match found for "+ state +" in " + str(location_words)
                        break
                #no match found
                if state_match is False:
                    state_match = False
                    #print "No state match in "+ str(location_words)
        
        if (state_match is True) and ('text' in tweets):
            tweet_state_list.append([tweets['text'], state])


    return tweet_state_list

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
    
    value = [ 
    ['ak', 'alaska'],
    ['al', 'alabama'],
    ['az', 'arizona'],
    ['ar', 'arkansas'],
    ['ca', 'california'],
    ['co', 'colorado'],
    ['ct', 'connecticut'],
    ['de', 'delaware'],
    ['fl', 'florida'],
    ['ga', 'georgia'],
    ['hi', 'hawaii'],
    ['id', 'idaho'],
    ['il', 'illinois'],
    ['in', 'indiana'],
    ['ia', 'iowa'],
    ['ks', 'kansas'],
    ['ky', 'kentucky'],
    ['la', 'louisiana'],
    ['me', 'maine'],
    ['md', 'maryland'],
    ['ma', 'massachusetts'],
    ['mi', 'michigan'],
    ['mn', 'minnesota'],
    ['ms', 'mississippi'],
    ['mo', 'missouri'],
    ['mt', 'montana'],
    ['ne', 'nebraska'],
    ['nv', 'nevada'],
    ['nh', 'hampshire'],
    ['nj', 'jersey'],
    ['nm', 'mexico'],
    ['ny', 'york'],
    ['nc', 'carolina'],
    ['nd', 'dakota'],
    ['oh', 'ohio'],
    ['ok', 'oklahoma'],
    ['or', 'oregon'],
    ['pa', 'pennsylvania'],
    ['ri', 'rhode'],
    ['sc', 'southcarolina'],
    ['sd', 'southdakota'],
    ['tn', 'tennessee'],
    ['tx', 'texas'],
    ['ut', 'utah'],
    ['vt', 'vermont'],
    ['va', 'virginia'],
    ['wa', 'washington'],
    ['dc', 'dc'],
    ['wv', 'westvirginia'],
    ['wi', 'wisconsin'],
    ['wy', 'wyoming']
    ]

    # { state: [abbr, score]}
    states_abbr_score_dict = {}
    for state_list in value:
        states_abbr_score_dict[state_list[1]] = [state_list[0], 0.0]

    affinity_dict = build_affinity_dict(sent_file)
    tweet_state_list = extract_tweet_list_and_state_from_json_file(tweet_file, states_abbr_score_dict)

    #tweet_state_list is a list of lists: [[tweet, state], [tweet, state], ...]

    for tweet_state in tweet_state_list: 
        tweet = tweet_state[0]
        state = tweet_state[1]

        score = grade_tweet(tweet, affinity_dict)
        states_abbr_score_dict[state][1] += score

    highest_score = 0
    happiest_state = 'none'
    for state in states_abbr_score_dict:
        score = states_abbr_score_dict[state][1]
        state_abbr = states_abbr_score_dict[state][0]

        if score > highest_score:
            happiest_state = state_abbr
            highest_score = score

    print happiest_state.upper()


if __name__ == '__main__':
    main()
