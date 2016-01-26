# Max Schwartz
# POS_Tagger.py
# Takes a sentence as input and returns the part of speech of each word.

import nltk

def addS(tagged_sents):
    '''Add open and close sentence tags'''
    
    for i in range(len(tagged_sents)):
        tagged_sents[i].append((u'</s>', u'CLOSE'))
        tagged_sents[i].insert(0, (u'<s>', u'OPEN'))

    return tagged_sents

def posBigram(tagged_sents):
    '''Create a dictionary of the likelyhood of a word being a specific pos given previous pos'''
    
    # create a list (set) of all possible tags
    tagList = []
    for sent in tagged_sents:
        for word in sent:
            tagList.append(word[1])
    tagList = set(tagList)
    
    # create a list (set) of all words in vocab
    wordList = []
    for sent in tagged_sents:
        for word in sent:
            wordList.append(word[0])
    wordList = set(wordList)
    wordList.remove('<s>')
    
    # create the dictionary
    # key1 is each word. value is another dic.
    # key2 is the previous part of speech. value is another dic again.
    # key3 is the current pos. value is the count of word with these parameters.
    posDict = {}
    for sent in tagged_sents:
        for i in range(1, len(sent)):
            if sent[i][0] in posDict:
                if sent[i-1][1] in posDict[sent[i][0]]:
                    posDict[sent[i][0]][sent[i-1][1]][sent[i][1]] += 1
                else:
                    posDict[sent[i][0]][sent[i-1][1]] = {tag:0 for tag in tagList}
                    posDict[sent[i][0]][sent[i-1][1]][sent[i][1]] += 1
            else:
                posDict[sent[i][0]] = {sent[i-1][1]:{tag:0 for tag in tagList}}
                posDict[sent[i][0]][sent[i-1][1]][sent[i][1]] += 1
    
    # Way too nested loop to get the actual percentages for each word's pos
    for word in wordList:
        for tag in tagList:
            if tag in posDict[word]:
                total = float(sum(posDict[word][tag].values()))
                for innerTag in tagList:
                    posDict[word][tag][innerTag] = posDict[word][tag][innerTag]/total
                    
    # create unigram pos count for backoff
    uni = {word : {tag : 0 for tag in tagList} for word in wordList}
    for sent in tagged_sents:
        for pair in sent:
            if pair[0] != '<s>':
                uni[pair[0]][pair[1]] += 1
    
    # get the most frequent pos for each word
    for word in wordList:
        uni[word] = uni[word].items()
        for i in range(len(uni[word])):
            uni[word][i] = list(uni[word][i])
            uni[word][i].reverse()
        uni[word].sort()
        uni[word] = uni[word][-1][1]
    
    return posDict, tagList, uni

def viterbize(new_sentence, pos, tags, uni):
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
    # this initial formatting takes some time
    text = list(nltk.corpus.brown.tagged_sents(tagset='universal'))
    train = addS(text)
    pos, tags, uni = posBigram(train)

    keepGoing = 'y'
    # might as well give the user a chance to enter multiple sentences
    # now they won't have to wait for the formatting every time
    while keepGoing == 'y':
        # get user's sentence
        newSent = raw_input("Enter sentence. Punctuation should have spaces: ")
        newSent = newSent.split()
        # add open and close sentence things
        newSent.insert(0, u'<s>')
        newSent.append(u'</s>')
        # run viterbi
        vet = viterbize(newSent, pos, tags, uni)
        # print the pos tag of each word
        # skip the CLOSE tag
        output = ""
        for tag in vet['</s>']['CLOSE']['path'][:-1]:
            output += tag + ' '
        print output
        # does the user want to continue?
        check = raw_input("Another sentence? (y/n)")
        keepGoing = check[0].lower()

main()