import string
import random
dig = string.ascii_letters + string.digits
import time
class ColNet:
    def about():
        print("YOU SERIOUS!")
    def generate_password(lenght):
        return ''.join(random.choice(dig) for _ in range(lenght))