from collections import defaultdict

wordunique = sorted(list(set([word.strip().lower() for word in open('words', 'r')])))

def signature(word):
    return ''.join(sorted(word))

words_bysig = defaultdict(list)

for word in wordunique:
    words_bysig[signature(word)].append(word)

def anagram_fast(word):
    return words_bysig[signature(word)]

anagrams = {word:anagram_fast(word) for word in wordunique if len(anagram_fast(word))>1}

dic_by_size = defaultdict(list)

for word in wordunique:
    dic_by_size[len(word)].append(word)

anagram_by_size = defaultdict(list)

for length, words in dic_by_size.items():
    anagram_by_size[length] = {word: len(anagram_fast(word))-1 for word in words if len(anagram_fast(word)) > 1}

anagram_by_size = defaultdict(list)
for length, words in dic_by_size.items():
    anagram_by_size[length] = sum(len(anagram_fast(word))-1 for word in words if len(anagram_fast(word)) > 1)/2


