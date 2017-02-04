import string
import random


def convertLetters(text: str):
    """
    Delete all spaces ponctuation and special characters of the string in parameters and return it
    :param text: string that could contain ponctuation space and special charachteres
    :return: return a string without ponctuation, space, and special charactere
    """
    string_to_return = ""
    alphabet = string.ascii_lowercase
    for letter in text.lower():
        if letter in alphabet:
            string_to_return += letter
    return string_to_return


def mix():
    """
    :return: string with all letter of alphabet in random order
    """
    alphabet = list(string.ascii_uppercase)
    string_to_return = ""
    for i in range(26):
        nb_random = random.randint(0,len(alphabet)-1)
        string_to_return += alphabet.pop(nb_random)
    return string_to_return


def createCylinder(file: str, n: int):
    """
    Crete a file with n lines where which line contain a alphabet in random order
    :param file: a string which contain the name of the file where the data will be store
    :param n: a positive integer which represent number of line store in the file
    """
    with open(file, 'w') as myfile:
        for i in range(n):
            myfile.write(mix()+"\n")


def loadCylender(file: str):
    """
    Load the file with the name place in parameters and return a dict with all line
    :param file: a string which is a file name
    :return: a dict with all lines of the file
    """
    key = {}
    try:
        with open(file, 'r') as myfile:
            for nb, line in enumerate(myfile):
                key[nb+1] = line[:-1]
    except:
        pass
    return key


def keyOK(key: list, n: int):
    """
    Check if the key is a permutation of all integers between 1 and n
    :param key: a list of integers
    :param n: an integer
    :return: True if the key is ok else False
    """
    list_to_compare = [i+1 for i in range(n)]
    if len(key) == len(list_to_compare) and set(list_to_compare) == set(key):
        return True
    return False


def createkey(n: int):
    """
    create a key
    :param n: a integer
    :return: a list of all number between 1 and n
    """
    number_list = [i for i in range(1, n+1)]
    new_key = []
    time_to_do = len(number_list)
    for i in range(time_to_do):
        nb_random = random.randint(0, len(number_list) - 1)
        new_key.append(number_list.pop(nb_random))
    return new_key


if __name__ == '__main__':
    pass
