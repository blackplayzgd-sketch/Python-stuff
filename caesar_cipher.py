def listToString(list, separator):
    string = ''
    
    for i in range(len(list)):
        string = string + list[i] + separator

    return string

def fisrtLetter(string):
    first_letter = string

    while len(first_letter) > 1:
        first_letter = first_letter[:len(first_letter) // 2]

    return first_letter

def ccipher(sentence, shift):  
    letterIndex = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'l': 11,
    'm': 12,
    'n': 13,
    'o': 14,
    'p': 15,
    'q': 16,
    'r': 17,
    's': 18,
    't': 19,
    'u': 20,
    'v': 21,
    'w': 22,
    'x': 23,
    'y': 24,
    'z': 25,
    }

    numIndex = {}
    for i in range(len(letterIndex.keys())):
        value, key = list(letterIndex.items())[i]
        numIndex.update({key: value})

    word_list = sentence.split(' ')
    ciphered_sentence = []

    for i in range(len(word_list)):
        word = word_list[i]
        ciphered_word = ''
        ciphered_letters = []
        
        for j in range(len(word)):
            first_letter = fisrtLetter(word)
            word = word.split(first_letter, 1)[1]

            if first_letter.isupper():
                first_letter = first_letter.lower()
                ciphered_letters.append(numIndex[(letterIndex[first_letter] + shift) % 26].upper())
            else:
                ciphered_letters.append(numIndex[(letterIndex[first_letter] + shift) % 26])
            
            
            
        ciphered_word.join(ciphered_letters)
        ciphered_sentence.append(listToString(ciphered_letters, ''))
    
    return listToString(ciphered_sentence, ' ')

sentence = str(input('Input a sentence to cipher: \n'))
shift = int(input('Input how many places to shift: \n'))

print('Ciphered sentence: \n' + ccipher(sentence, shift))




