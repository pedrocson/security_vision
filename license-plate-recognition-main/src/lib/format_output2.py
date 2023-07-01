#import colorama
import colorama
from colorama import Fore, Style

colorama.init()

header = ['Image', 'Plate']


def fixed_length(text, length):
    if len(text) > length:
        text = text[:length]
    elif len(text) < length:
        text = (text + " " * length)[:length]
    return text


def format_output2(data):
    print("━" * 46)
    print("┃", end=" ")
    for column in header:
        print(fixed_length(column, 20), end=" ┃ ")
    print()
    print("━" * 46)

    for row in data:
        print("┃", end=" ")
        for column in row:
            if column == 'AUTHORIZED':
                print(Fore.GREEN + fixed_length(column, 20) + Style.RESET_ALL, end=" ┃ ")
            elif column == 'NOT AUTHORIZED':
                print(Fore.RED + fixed_length(column, 20) + Style.RESET_ALL, end=" ┃ ")
            else:
                print(fixed_length(column, 20), end=" ┃ ")
        print()
    print("━" * 46)
