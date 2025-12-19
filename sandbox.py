

def say_blyat(func):
    def wrapper():
        print("Blyat")
        func()
        print("how are you?")
    return wrapper

@say_blyat
def say_hello():
    print("Hello")

say_hello()


def f():
    try:
        return print("Clgfvjhgka"), 2
    except:
        "dfas"


f()