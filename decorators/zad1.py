from functools import wraps

"""
Napisz dekorator @to_list,  który opakowuje funkcję zwracającą tekst (iterable) oraz zwraca jej znaki (elementy) w postaci jednowymiarowej listy.

Przykład:
"""

def to_list(func):
    lista =[]
    @wraps(func)
    def wrapper():
        slowo = func()
        for i in range(len(slowo)):
            lista.append(slowo[i])
        return lista
    return wrapper



@to_list
def say_python():
    return 'Python'


#assert say_python() == ['P', 'y', 't', 'h', 'o', 'n']

print(say_python())
