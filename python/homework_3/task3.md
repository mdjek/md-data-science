#### Task 3

```python
import requests
from bs4 import BeautifulSoup


def fetch_data(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"При запросе данных возникла ошибка: {e}")
        return ""


def parse_data(url: str, tag_name: str) -> list:
    try:
        html = fetch_data(url)
        soup = BeautifulSoup(html, "html.parser")

        nodeList = soup.find_all(tag_name)
        return [node.text for node in nodeList]
    except Exception as e:
        print(f"При парсинге возникла ошибка: {e}")
        return []


# Пример использования
print(parse_data("https://loremipsum.io/ru", "h2"))
```
