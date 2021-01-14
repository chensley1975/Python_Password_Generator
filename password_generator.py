import random
import csv

def Create_Password(pLength):

    jumbled = []
    password = ''
    lower_char = 'abcdefghijklmnopqrstuvwxyz'
    upper_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    number_char = '0123456789'
    special_char = '!@#$%^&*'
    lower = 0
    upper = 0
    number = 0
    special = 0

    if pLength > 8:
        special = 2
    else:
        special = 1
    upper = int(pLength/4)
    number = int(pLength/4)
    lower = pLength - (special + upper + number)

    for l in range(lower):
        jumbled.append(random.choice(lower_char))

    for u in range(upper):
        jumbled.append(random.choice(upper_char))

    for n in range(number):
        jumbled.append(random.choice(number_char))

    for s in range(special):
        jumbled.append(random.choice(special_char))
            
    for p in range(pLength):
        c = len(jumbled)
        if c > 1:
            d = random.randint(0, c-1)
            password += jumbled[d]
            jumbled.pop(d)
        else:
            password += jumbled[0]
            jumbled.pop(0)

    return password

Create_Password(12)
