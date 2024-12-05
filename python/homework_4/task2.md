#### Task 2

```python
import itertools
from typing import Iterable


def infinite_number_generator():
    for number in itertools.count(start=1, step=1):
        yield number


def combine_iterators(*iterators: Iterable) -> itertools.chain:
    for iterator in iterators:
        if not isinstance(iterator, Iterable):
            raise TypeError("Аргументы не являются итерируемыми")
    try:
        return itertools.chain(*iterators)
    except Exception as e:
        raise Exception(f"Возникла ошибка при объединении итераторов: {e}")


def apply_function_to_iterator(iterator, func) -> list:
    full_list = []

    for item in iterator:
        try:
            result = func(item)
            full_list.append(result)
        except Exception as e:
            print(f"Ошибка при обработке элемента {item}: {e}")

    return full_list


# Бесконечный генератор чисел
generator = infinite_number_generator()
for _ in range(10):
    print(next(generator))

# Пример объединения нескольких итераторов
list1 = [1, 2, 3]
list2 = ["str1", "str2", "str3"]
combine_result = combine_iterators(list1, list2)
print(combine_result)

# Применение функции к каждому элементу в итераторе
print(apply_function_to_iterator(combine_result, lambda x: x + x))
```
