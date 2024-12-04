#### Task 1

```python
import datetime

FORMAT_DATE_STR = "%Y-%m-%d %H:%M:%S"


def get_current_datetime(format_string=FORMAT_DATE_STR) -> str:
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime(format_string)


def convert_string_to_datetime(date_string, format_string=FORMAT_DATE_STR):
    try:
        return datetime.datetime.strptime(date_string, format_string)
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте формат: 'YYYY-MM-DD HH:MM:SS'")


def calculate_date_difference(date1: str, date2: str, format_string=FORMAT_DATE_STR) -> str:
    try:
        datetime1 = convert_string_to_datetime(date1, format_string)
        datetime2 = convert_string_to_datetime(date2, format_string)

    except ValueError:
        raise ValueError("Неверный формат даты. Используйте формат: 'YYYY-MM-DD HH:MM:SS'")

    return datetime2 - datetime1


# Отображение текущей даты и времени
print(f"Текущая дата: {get_current_datetime()}")

# Преобразование строки в объект даты и времени
date_string = "2024-11-04 10:00:00"
print(f"Сконвертированная дата, время: {convert_string_to_datetime(date_string)}")

# Вычисление разницы между двумя датами
date_string1 = "2024-10-15 14:00:15"
date_string2 = "2024-10-25 18:30:35"
print(f"Временная разница между датами: {calculate_date_difference(date_string1, date_string2)}")
```