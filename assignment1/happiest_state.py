import sys
import json
def b_af_dt(afinnfile):
    scs = {} 
    for line in afinnfile:
        term, sc  = line.split("\t")  
        scs[term] = int(sc)  
    return scs
def exx(twfile, ss):
    tws = {} 
    tw_s_lt = []
    for line in twfile:
        s_match = False
        tws = json.loads(line)
        if 'user' in tws:
            if 'location' in tws['user']:
                l_wo = tws['user']['location'].split(" ")
                for w in l_wo:
                    if w.lower() in ss:
                        s = w.lower() 
                        if (s == 'dakota' or s == 'carolina'):
                            for w in l_wo:
                                if w.lower() == 'north':
                                    s = s
                                    s_match = True
                                    break
                                if w.lower() == 'south':
                                    s = 'south'+s
                                    s_match = True
                                    break
                            if s_match is False:
                                break
                        if (s == 'virginia'):
                            for w in l_wo:
                                if w.lower() == 'west':
                                    s = 'westvirginia'
                                    break
                        if (s == 'mexico' or s == 'york'):
                            for w in l_wo:
                                if w.lower() == 'new':
                                    s_match = True
                                    break
                            if s_match is False:
                                break
                        s_match = True
                        break
                if s_match is False:
                    s_match = False
        if (s_match is True) and ('text' in tws):
            tw_s_lt.append([tws['text'], s])
    return tw_s_lt
def grade_tw(tw, af_dt):
    sc = 0.0
    ws = tw.split(" ")
    for w in ws:
        w = w.lower()
        if w in af_dt:
            sc += af_dt[w]
    return sc

def main():
    sent_file = open(sys.argv[1])
    tw_file = open(sys.argv[2])
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
    ss_abbr_sc_dt = {}
    for s_lt in value:
        ss_abbr_sc_dt[s_lt[1]] = [s_lt[0], 0.0]
    af_dt = b_af_dt(sent_file)
    tw_s_lt = exx(tw_file, ss_abbr_sc_dt)
    for tw_s in tw_s_lt: 
        tw = tw_s[0]
        s = tw_s[1]
        sc = grade_tw(tw, af_dt)
        ss_abbr_sc_dt[s][1] += sc
    highest_sc = 0
    happiest_s = 'none'
    for s in ss_abbr_sc_dt:
        sc = ss_abbr_sc_dt[s][1]
        s_abbr = ss_abbr_sc_dt[s][0]
        if sc > highest_sc:
            happiest_s = s_abbr
            highest_sc = sc
    print happiest_s.upper()
if __name__ == '__main__':
    main()
