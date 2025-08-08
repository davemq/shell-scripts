import sys
import random

text = sys.stdin.read()

words = text.split()

chain = dict()

# - If a words is not yet in chain, add it as a key
# - add the next word to the value

prev1 = None
prev2 = None
chain[(prev1,prev2)] = []

for word in words:
    if (prev1,prev2) not in chain:
        chain[(prev1,prev2)] = [word]
    else:
        chain[(prev1,prev2)].append(word)
    prev1 = prev2
    prev2 = word
    
if (prev1,prev2) not in chain:
    chain[(prev1,prev2)] = [None]
else:
    chain[(prev1,prev2)].append(None)

random.seed()

prev1 = None
prev2 = None
word = random.choice(chain[(prev1,prev2)])
while word is not None:
    print(word, end=' ')
    prev1 = prev2
    prev2 = word
    word = random.choice(chain[(prev1,prev2)])
print()
