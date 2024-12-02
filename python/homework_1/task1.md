```python
class Animal:
    def __init__(
        self,
        name: str,
        sound: str,
    ) -> None:
        self.name = name
        self.sound = sound

    def makesound(self) -> None:
        return f"{self.name} says: {self.sound}!"


class Cat(Animal):
    def __init__(self, name: str, sound: str, color: str) -> None:
        super().__init__(name, sound)
        self.color = color

    def makesound(self) -> None:
        super().makesound()
        print(f"{self.color} {super().makesound()}")


class Dog(Animal):
    def __init__(self, name: str, sound: str, color: str) -> None:
        super().__init__(name, sound)
        self.color = color

    def makesound(self) -> None:
        super().makesound()
        print(f"{self.color} {super().makesound()}")


cat = Cat("Cat", "Meow", "Black")
dog = Dog("Dog", "Woof", "White")

cat.makesound()
dog.makesound()
```
