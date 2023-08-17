import random
import string

def generate_invite_code():
    print(random.choice(string.digits + string.ascii_letters))
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


print(generate_invite_code())

