#### Task 2

```python
import string
from collections import Counter


def clean_punctuation(str: str):
    return str.translate(str.maketrans("", "", string.punctuation))


def get_count_words(text: str, is_uniq_only=False):
    if not text:
        return 0

    cleaned_text = clean_punctuation(text)
    words = cleaned_text.split()

    word_counts = Counter(words)

    # Возвращаем количество слов (уникальных или всех)
    return len(word_counts if is_uniq_only else words)


# Пример использования
text = "Был холодный осенний день. Дул холодный осенний ветер."
word_count = get_count_words(text)
unique_word_count = get_count_words(text, True)
print(f"Всего слов: {word_count}; Количество уникальных слов: {unique_word_count}") # Всего слов: 9; Количество уникальных слов: 6
```
