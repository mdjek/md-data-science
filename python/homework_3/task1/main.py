# main.py
from my_math.sum_numbers import SumNumbers

if __name__ == "__main__":
    # Создаем экземпляр класса SumNumbers
    calculator = SumNumbers()

    # Вычисляем сумму чисел в списке
    result = calculator.get_sum((1, 2, 3, 4, 5))
    print(f"Сумма чисел: {result}")
