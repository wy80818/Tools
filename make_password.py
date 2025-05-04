import random
import sys

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
NUMBERS = "0123456789"
ALL = {"LOWERCASE": LOWERCASE, "UPPERCASE": UPPERCASE, "SYMBOLS": SYMBOLS, "NUMBERS": NUMBERS}

def generate_password(length, o_chars):
    """
    Description: Main password generation algorithm.
    :param length: Password length.
    :param o_chars: Characters to ignore (if the user put any).
    :return chars: Generated password to return.
    """
    # Randomly chooses a character from a random list inside ALL list
    chars = ''
    i = 0
    while i < length:
        randomizer = random.randint(0, sys.maxsize) % len(ALL)
        char = list(ALL.values())[randomizer][random.randint(0, len(list(ALL.values())[randomizer]) - 1)]
        if char not in o_chars:
            chars += char
            i += 1

    return chars


def analyze(password):
    """
    Description: Calculates percentages between symbols, numbers, 
    lowercase and uppercase characters, and informs the user if any are low or too low.
    :param password: The generated password.
    :return None:
    """
    counts = [0] * len(ALL)

    # Gets the counts of each char type
    for char in password:
        for i in range(len(ALL)):
            if char in list(ALL.values())[i]:
                counts[i] += 1

    # Outputs percentages
    print(f"PASSWORD:\n{password}\n")
    for i in range(len(counts)):
        calc = 100 * (counts[i]/len(password))
        print(f"{list(ALL.keys())[i]}: {calc:.2f}%", end=" ")
        if calc <= 5:
            print("VERY LOW!")
        elif calc <= 15:
            print("Low.")
        else:
            print()
    

if __name__ == '__main__':
    random.seed()  # Seed is set to system time

    # Gets user inputted length, retries if bad number
    user_length = 0
    while not user_length:
        try:
            user_length = int(input("Please enter a password length (>8 recommended!): "))
        except ValueError as e:
            print("Not a number!")

    # Gets user inputted omitted characters, these chars will NOT be generated in the password.
    omitted_chars = input("Please enter any chars to omit (empty input for none): ")

    # Generates a new password each time user presses enter.
    try: 
        while True:
            print("=================================\n")
            password = generate_password(user_length, omitted_chars)
            analyze(password)
            input("CTRL+C to stop, ENTER to continue >> ")
    except KeyboardInterrupt as e:
        print("Exitting...")
    