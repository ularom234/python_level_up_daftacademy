import datetime  # do not change this import, use datetime.datetime.now() to get date
from functools import wraps


def is_correct(*args):
    def decorator(func):
        @wraps(func)
        def wrapper():
            result = func()
            for arg in args:
                if arg in result.keys():
                    continue
                else:
                    return None
            return result

        return wrapper

    return decorator


def add_date(format):
    def decorator(func):
        @wraps(func)
        def wrapper():
            result = func()
            d = datetime.datetime.now().strftime(format)
            result['date'] = d

            return result

        return wrapper

    return decorator


"""
Napisz dekorator @add_date,  który opakowuje funkcję zwracającą słownik. Dekorator ma dodać aktualną datę do zwracanego przez dekorowaną funkcję słownika w formacie podanym jako argument dekoratora.

Użyj modułu datetime korzystając z datetime.datetime.now() do pobrania aktualnej daty. Więcej informacji o formatowaniu znajdziesz tutaj:
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

%A - day
%d - day of the month
%B - Month, full name
%Y - year


Przykład:  """


@add_date('%A %d. %B %Y')
def get_data():
    return {1: 2, 'name': 'Jan'}


print(get_data())

assert get_data() == {1: 2, 'name': 'Jan', 'date': 'Saturday 23. March 2019'}

print("wykonalem")

"""
Dodatkowo sprawdź czy możesz użyć dwóch dekoratorów: @add_date oraz @is_correct z poprzedniego zadania oraz zastanów się w jakiej kolejności zostaną wywołane oraz czy wynik będzie poprawny.

Przykład:"""


@is_correct('date')
@add_date('%A %d. %B %Y')
def get_data():
    return {1: 2, 'name': 'Jan'}


print(get_data())
print("tak sie da?")


@add_date('%A %d. %B %Y')
@is_correct('date')
def get_data():
    return {1: 2, 'name': 'Jan'}


print(get_data())
