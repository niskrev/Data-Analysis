# with open('words','r') as f:
#     wordlist = f.readlines()
#
# wordclean = [word.strip().lower() for word in wordlist]
# wordunique = list(set(wordclean))
# wordunique.sort()


wordunique = sorted(list(set([word.strip().lower() for word in open('words', 'r')])))

def signature(word):
    return ''.join(sorted(word))

import collections
words_bysig = collections.defaultdict(list)

for word in wordunique:
    words_bysig[signature(word)].append(word)

def anagram_fast(word):
    return words_bysig[signature(word)]

def anagram(word):
    return [w for w in wordunique if signature(w)==signature(word)]


anagrams = {word:anagram_fast(word) for word in wordunique if len(anagram_fast(word))>1}