# Max Schwartz
# POS_Tagger.py
# Takes a sentence as input and returns the part of speech of each word.

import json

def calculate_matrix(new_sentence, pos, tags, uni):
    '''Create and calculate the paths. Return the best path.'''
    
    # set up initial path-tracker
    matrix = {word : {tag : {'prob' : 0, 'path' : []} for tag in tags} for word in new_sentence}
    # OPEN should have prob of 1
    matrix['<s>']['OPEN']['prob'] = 1
    
    # loop through to get the max prob for each pos for each word
    for i in range(1, len(new_sentence)):
        # see if word is in vocab
        if new_sentence[i] in pos:
            # we know the word is in the vocab, 
            # but has it ever been seen after any of the potential candidates
            # for previous pos?
            found = False
            # look at each possible tag for the current word
            for tag in tags:
                # we want to find the tags with a > 0 prob
                best = 0.0
                # we want to remember the best path to the best tag
                path = []
                # initialize a variable to remember current prob
                current = 0.0
                # loop through the previous possible tags
                for prevTag in tags:
                    # if the previous tag is a known tag that comes before the current word,
                    # see what the chances are of that tag leading to the current one we are looking at
                    if prevTag in pos[new_sentence[i]]:
                        current = pos[new_sentence[i]][prevTag][tag] * matrix[new_sentence[i-1]][prevTag]['prob']
                        # if this prob is better than our previous best, it is the new one to beat
                        if current > best:
                            # if we found a prob > 0, we now know that
                            # one of the previous pos candidates has been seen before
                            found = True
                            best = current
                            path = matrix[new_sentence[i-1]][prevTag]['path'][0:]
                            path.append(tag)
                # update prob and path for current tag
                matrix[new_sentence[i]][tag]['prob'] = best
                matrix[new_sentence[i]][tag]['path'] = path
            # if the word has been seen, but never after any of the non-zero prob previous pos candidates
            # we back off to its most common unigram pos
            if not found:
                uniPOS = uni[new_sentence[i]]
                prevBest = 0
                for tagsAgain in tags:
                    if matrix[new_sentence[i-1]][tagsAgain]['prob'] > prevBest:
                        prevBest = matrix[new_sentence[i-1]][tagsAgain]['prob']
                        path = matrix[new_sentence[i-1]][tagsAgain]['path'][0:]
                matrix[new_sentence[i]][uniPOS]['prob'] = prevBest
                path.append(uniPOS)
                matrix[new_sentence[i]][uniPOS]['path'] = path
        # if word is oov, assume it's a noun
        else:
            for tag in tags:
                best = 0
                path = []
                for prevTag in tags:
                    if tag == 'NOUN':
                        current = 1.0 * matrix[new_sentence[i-1]][prevTag]['prob']
                    else:
                        current = 0.0
                    if current > best:
                        best = current
                        path = matrix[new_sentence[i-1]][prevTag]['path'][0:]

                path.append(tag)
                matrix[new_sentence[i]][tag]['prob'] = best
                matrix[new_sentence[i]][tag]['path'] = path
    
    return matrix

def main():
    with open('data/pos.json', 'r') as pos_data:
        pos = json.load(pos_data)
    with open('data/tags.json', 'r') as tag_data:
        tags = json.load(tag_data)
    with open('data/uni.json', 'r') as uni_data:
        uni = json.load(uni_data)

    keepGoing = 'y'
    # might as well give the user a chance to enter multiple sentences
    while keepGoing == 'y':
        # get user's sentence
        # need to fix the punctuation space thing
        # probably force insert a space before final punctuation
        # or use a better tokenizer than just splitting on spaces
        newSent = input("Enter sentence. Punctuation should have spaces: ")
        newSent = newSent.split()
        # add open and close sentence things
        newSent.insert(0, u'<s>')
        newSent.append(u'</s>')
        # run viterbi
        vet = calculate_matrix(newSent, pos, tags, uni)
        # print the pos tag of each word
        # skip the CLOSE tag
        output = ""
        for tag in vet['</s>']['CLOSE']['path'][:-1]:
            output += tag + ' '
        print(output)
        # does the user want to continue?
        check = input("Another sentence? (y/n)")
        keepGoing = check[0].lower()

if __name__ == '__main__':
    main()