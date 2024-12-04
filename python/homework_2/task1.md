#### Task 1

```python
def read_numeric_lines(file_path: str) -> None:
    try:
        with open(file_path, "r") as data:
            lineList = data.readlines()

            if len(lineList) == 0:
                print(f"Файл '{file_path}' пустой")

            for index, line in enumerate(lineList):
                try:
                    cleared_str = line.strip()

                    if cleared_str.isdigit():
                        print(cleared_str)
                    else:
                        float(cleared_str)
                        print(float(cleared_str))
                except ValueError:
                    raise TypeError(f"Строка #{index+1} '{cleared_str}' содержит нечисловое значение")
    except FileNotFoundError:
        raise print(f"Файл '{file_path}' не найден")


# Пример использования
read_numeric_lines("data.txt")
```
