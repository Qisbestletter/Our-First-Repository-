
def count_vowels(word):
    count = 0
    vowels = "aeiouy"
    for letter in word:
        if letter.lower() in vowels:
            count += 1
    return count
