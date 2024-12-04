```python
class DataBuffer:
    def __init__(self):
        self.buffer = []

    def add_data(self, data) -> None:
        self.buffer.append(data)
        if len(self.buffer) >= 5:
            print("Буфер заполнен")
            self.buffer.clear()

    def get_data(self) -> list:
        if not self.buffer:
            print("В буфере данные отсутствуют")
        else:
            return self.buffer

# Пример использования
buffer = DataBuffer()
buffer.add_data("record1")
buffer.add_data("record2")

print(buffer.get_data())
```
