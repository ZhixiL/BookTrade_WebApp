inp = ["this","is","an","example"]
output = dict()
vowels = ["a","e","i","o","u"]
def vowelCheck(inp):
    lWord = inp.lower()
    count = 0
    for x in vowels:
        if x in lWord:
            count = count + 1
    return count

for word in inp:
    output[word] = vowelCheck(word)

print(output)

