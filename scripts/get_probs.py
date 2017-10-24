# Max Schwartz
# POS_Tagger.py
# Takes a sentence as input and returns the part of speech of each word.

import json
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
        uni[word] = list(uni[word].items())
        for i in range(len(uni[word])):
            uni[word][i] = list(uni[word][i])
            uni[word][i].reverse()
        uni[word].sort()
        uni[word] = uni[word][-1][1]
    
    return posDict, list(tagList), uni

def main():
    # this initial formatting takes some time
    text = list(nltk.corpus.brown.tagged_sents(tagset='universal'))
    train = addS(text)
    pos, tags, uni = posBigram(train)
    with open('data/pos.json', 'w') as pos_out:
        json.dump(pos, pos_out, indent=4, sort_keys=True)
    with open('data/tags.json', 'w') as tags_out:
        json.dump(tags, tags_out, indent=4, sort_keys=True)
    with open('data/uni.json', 'w') as uni_out:
        json.dump(uni, uni_out, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()