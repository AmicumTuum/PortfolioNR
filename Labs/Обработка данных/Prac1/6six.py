def is_polynom(word):
    flip = word.lower()
    flip = ''.join(c for c in word if c.isalnum())
    return flip == word[::-1]

word = str(input())    
if is_polynom(word):
    print("да")
else:
    print("нет")