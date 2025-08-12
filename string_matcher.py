from difflib import SequenceMatcher

a='harsh'
b='h'
print(SequenceMatcher(None, a, b).ratio())