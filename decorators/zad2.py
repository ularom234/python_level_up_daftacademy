from functools import wraps

"""
Napisz dekorator @is_correct,  który opakowuje funkcję zwracającą słownik. Dekorator ma sprawdzić czy w słowniku znajdują się klucze zawarte w argumentach dekoratora. Jeśli tak niech zwróci ten słownik, jeśli nie, niech zwraca wartość None.

Przykład:


"""
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


@is_correct('first_name', 'last_name')
def get_data():
    return {
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'email': 'jan@kowalski.com'
    }


@is_correct('first_name', 'last_name', 'email')
def get_other_data():
    return {
        'first_name': 'Jan',
        'email': 'jan@kowalski.com'
    }

print(get_data())
print(get_other_data())


assert get_data() == {
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'email': 'jan@kowalski.com'
    }


assert get_other_data() is None
