def count_word_frequency(strings):
    word_freq = {}
    for string in strings:
        words = string.split()
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    return word_freq

strings = ["это тест", "это слово", "тест слово тест"]
result = count_word_frequency(strings)
print(result)