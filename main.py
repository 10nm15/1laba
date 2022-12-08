import operator
import numpy as np

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def main():
    print("Введите 1 если вы хотите зашифровать слово, 2 если расшифровать вручную или 3 если взломать такое слово: ")
    flag = input()
    if flag == "1":
        encryptInit()
    elif flag == "2":
        decipherInit()
    elif flag == "3":
        autoDecipherInit()
    else:
        print("Введено неверное число, попробуйте снова: ")
        main()


def encryptInit():
    wordList = input("Введите сообщение которое хотите зашифровать: ").lower().split()
    shift = int(input("Введите сдвиг (0 - 33): "))
    if shift > len(ALPHABET):
        print("Введено неверное число! Попробуйте снова!")
        wordList = ""
        encryptInit()
    else:
        print("Ваше зашифрованное слово: ", " ".join(encrypyedMessage(wordList, shift)))


def decipherInit():
    wordList = input("Введите сообщение которое хотите расшифровать: ").lower().split()
    shift = int(input("Введите сдвиг (0 - 33): "))
    if shift > len(ALPHABET):
        print("Введено неверное число! Попробуйте снова!")
        wordList = ""
        decipherInit()
    else:
        print("Рашифрованное слово: ", " ".join(encrypyedMessage(wordList, len(ALPHABET) - shift)))


def encrypyedMessage(wordList, shift):
    newList = []
    for i in range(len(wordList)):
        word = wordList[i]
        newList.append(encrypt(word, shift))
    return newList


def encrypt(word, shift):
    newWord = ""
    for i in range(len(word)):
        for j in range(len(ALPHABET)):
            if word[i] == ALPHABET[j]:
                newWord = newWord + ALPHABET[(j + shift) % len(ALPHABET)]
    return newWord


def dicRateFill(dic):
    for i in range(1, len(ALPHABET) + 1):
        dic[i] = 0


def abRating(wordList, dic):
    for shift in range(1, len(ALPHABET) + 1):
        dic[shift] = localRating(wordList, shift)


def localRating(wordList, shift):
    shiftRating = 0
    encryptedWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in encryptedWords:
        shiftRating += wordRating(word)
    return shiftRating


def wordRating(word):
    wordRate = 0
    glasnye = "аеиоуыэюяё"
    soglasnye = "бвгджзйклмнпрстфхцчшщъь"
    for i in range(len(word) - 1):
        if (soglasnye.__contains__(word[i])) and (glasnye.__contains__(word[i + 1])):
            wordRate += 1
    return wordRate


def freqRating(wordList, dic):
    string = "".join(wordList)
    frequencies = np.zeros(len(ALPHABET), dtype=int)
    max = -1
    maxi = 0
    for letter in string:
        index = ALPHABET.index(letter)
        frequencies[index] += 1

    for i in range(len(frequencies)):
        if max < frequencies[i]:
            max = frequencies[i]
            maxi = i

    maxFreqLetter = ALPHABET[maxi]
    for shift in range(1, len(ALPHABET) + 1):
        if encrypt(maxFreqLetter, len(ALPHABET) - shift) == "о":
            dic[shift] **= 1.2
            break


def printHighRated(wordList, dic):
    topShifts = []
    sortedDic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
    sum = 0.0000001
    for j in range(0, len(ALPHABET)):
        sum += sortedDic[j][1]
    for i in range(3):
        print(" ".join(encrypyedMessage(wordList, len(ALPHABET) - sortedDic[i][0])),
              " \n(вероятность того что этот ответ правильный: ", int((sortedDic[i][1] / sum) * 100), "%)")
    return topShifts


def removingTrash(wordList, dic):
    for shift in range(1, len(ALPHABET) + 1):
        clearPretext(wordList, dic, shift)
        clearPrefix(wordList, dic, shift)
        clearPostfix(wordList, dic, shift)
        clearSoftness(wordList, dic, shift)


def clearPretext(wordList, dic, shift):
    pretext = "йценгшщзхъфыпрлджчмтьбюё"
    decipherWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in decipherWords:
        if len(word) == 1 and pretext.__contains__(word):
            dic[shift] = 0
            break


def clearPrefix(wordList, dic, shift):
    wrongPrefix = "ъь"
    decipherWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in decipherWords:
        if wrongPrefix.__contains__(word[0]):
            dic[shift] = 0
            break


def prefixRating(wordList, dic):
    for shift in range(1, len(ALPHABET) + 1):
        dic[shift] += shiftPrefixRating(wordList, shift)


def shiftPrefixRating(wordList, shift):
    prefixRate = 0
    truePrefix = ["без", "бес", "во", "воз", "вос", "возо", "вз", "вс", "вы", "до", "за", "из", "ис", "изо", "на"
        , "наи", "недо", "над", "надо", "не", "низ", "нис", "низо", "об", "обо", "обез", "обес", "от", "ото"
        , "па", "пра", "по", "под", "подо", "пере", "пре", "пред", "предо", "при", "про", "раз", "рас", "разо"
        , "со", "су", "через", "черес", "ана", "анти", "архи", "гипер", "гипо", "де", "дез", "дис"
        , "ин", "интер", "инфра", "квази", "кило", "контр", "макро", "микро", "мега", "мата", "мульти", "орто"
        , "пан", "пара", "пост", "прото", "ре", "суб", "супер", "транс", "ультра", "экстра", "экс", "взо", "среди"
        , "роз", "рос", "раз", "рас", "абоба"]

    decipherWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in decipherWords:
        for prefix in truePrefix:
            if word.startswith(prefix):
                prefixRate += len(prefix)
    return prefixRate


def clearPostfix(wordList, dic, shift):
    postfix = "ъ"
    decipherWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in decipherWords:
        if postfix.__contains__(word[len(word) - 1]):
            dic[shift] = 0
            break


def clearSoftness(wordList, dic, shift):
    wrongs = ["чя", "щя", "чю", "щю", "жы", "шы", "ьъ", "ъь", "ъо", "ъэ", "ъы", "ъй", "ъц", "ъу"
        , "ък", "ън", "ъг", "ъш", "ъщ", "ъз", "ъх", "ъф", "ъв", "ъа", "ъп", "ър", "ъъ", "ёъ"
        , "ъл", "ъд", "ъж", "ъч", "ъс", "ъм", "ъи", "ът", "ъб", "яъ", "иъ", "уъ"
        , "еъ", "ыъ", "аъ", "оъ", "эъ", "юъ", "эь", "йй", "цй", "кй", "нй", "гй", "шй"
        , "шй", "зй", "хй", "ъй", "фй", "вй", "пй", "рй", "лй", "дй", "жй", "чй", "сй"
        , "мй", "тй", "ьй", "бй", "кы", "кя", "йы", "йе", "йа", "йю", "йь"]

    decipherWords = encrypyedMessage(wordList, len(ALPHABET) - shift)
    for word in decipherWords:
        for wrong in wrongs:
            if word.__contains__(wrong):
                dic[shift] = 0
                break


def autoDecipherInit():
    wordList = input(
        "Введите сообщение которое хотите расшифровать (чем больше сообщение, тем больше шанс найти ответ): \n").lower().split()
    dicRate = {}
    dicRateFill(dicRate)
    abRating(wordList, dicRate)
    freqRating(wordList, dicRate)
    prefixRating(wordList, dicRate)
    removingTrash(wordList, dicRate)
    print("Вероятно правильный ответ находится среди этих вариантов: \n")
    printHighRated(wordList, dicRate)


main()
