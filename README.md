# POS_Tagger
Tags part of speech for user input:<br />
"This is an example" -> "DET VERB DET NOUN"

This project was originally an assignment for a graduate class. It trains on the Brown Corpus (https://en.wikipedia.org/wiki/Brown_Corpus) via NLTK (http://www.nltk.org/book/ch02.html). I chose to use the Universal Tagset (http://universaldependencies.org/u/pos/), as it is the closest to how most people think of part of speech. The probablities for each word being each part of speech are calculated as well as these parts of speech following each other part of speech (hence the nested dictionaries). Using a dynamic algorithm based on the Viterbi algorithm (https://en.wikipedia.org/wiki/Viterbi_algorithm), the user's sentence is analyzed and tagged based on the training data. 

### Accuracy
Dividing the corpus into a randomized 90% train set and 10% test set revealed error rates between 4.3% and 4.4%. I'm pretty happy with >95% accuracy.

### Next Steps
- Improved backoff (current version assumes out of vocabulary words are nouns)
- Test against other corpora/include other corpus data in training
- Improved tokenization

### Required Libraries
At the moment, NLTK is the only non-standard library, and it is only used in the probability generation script (`scripts/get_probs.py`). The core code (`POS_Tagger.py`) may eventually require NLTK depending on the tokenizer that is used, but for the moment requires no non-standard libraries.
