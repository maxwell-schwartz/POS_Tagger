# POS_Tagger
Tags part of speech for user input.

This project was originally an assignment for a graduate class. It trains on the Brown Corpus (https://en.wikipedia.org/wiki/Brown_Corpus) via NLTK (http://www.nltk.org/book/ch02.html). I chose to use the Universal Tagset, as it is the closest to how most people think of part of speech. The probablities for each word being each part of speech are calculated as well as these parts of speech following each other part of speech (hence the nested dictionaries). Using a dynamic algorithm based on the Viterbi algorithm (https://en.wikipedia.org/wiki/Viterbi_algorithm), the user's sentence is analyzed and tagged based on the training data. 

<h3>Accuracy</h3>
Dividing the corpus into a randomized 90% train set and 10% test set revealed error rates between 4.3% and 4.4%. I'm pretty happy with >95% accuracy.

<h3>Next Steps</h3>
I am aware that the initial setup takes at least 30 seconds, which is too long. I am going to try pickling the analyzed and formatted corpus data. Hopefully that will help.

Additionally, a good portion of the errors appear to come from out of vocabulary words. My current backoff system just assumes these are nouns, which do make up a large percentage of the new words, but obviously not all. Applying some sort of morphological analysis could help cut down on these error.
