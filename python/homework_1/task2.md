```python
import logging

# Настройка логирования
logging.basicConfig(
    filename="products.log", level=logging.INFO, format="%(asctime)s — %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def increment_quantity(self, amount):
        if amount > 0:
            self.quantity += amount
            logging.info(f"Количество товара «{self.name}» увеличено на {amount}. Текущее количество: {self.quantity}")
        else:
            logging.warning("Значение для увеличения должно быть > 0.")

    def decrement_quantity(self, amount):
        if amount > 0:
            if self.quantity >= amount:
                self.quantity -= amount
                logging.info(
                    f"Количество товара «{self.name}» уменьшено на {amount}. Текущее количество: {self.quantity}"
                )
            else:
                logging.warning(f"Недостаточно товара «{self.name}» на складе для уменьшения на {amount}.")
        else:
            logging.warning("Значение для уменьшения должно быть > 0.")

    def calc_total_cost(self):
        total_cost = self.quantity * self.price
        logging.info(f"Общая стоимость товара «{self.name}»: {total_cost} units")

        return total_cost


class Seller:
    def __init__(self, name):
        self.name = name
        self.sales_report = []

    def sell_product(self, product, quantity):
        if product.quantity >= quantity:
            product.decrement_quantity(quantity)

            summ = quantity * product.price
            self.sales_report.append((product.name, quantity, summ))
            logging.info(f"Продавец «{self.name}» продал {quantity} товара «{product.name}». Сумма: {summ} units")
        else:
            logging.warning(f"Товара «{product.name}» для продажи недостаточно.")

    def generate_sales_report(self):
        report = f"Отчет о реализации товаров (продавец: {self.name}):\n"

        for sale in self.sales_report:
            report += f"Товар: «{sale[0]}», Количество: {sale[1]}, Сумма: {sale[2]} units \n"

        logging.info(f"Сформирован отчёт о реализации товаров (продавец «{self.name}»).")
        return report


class Warehouse:
    def __init__(self):
        # Хранилище для товаров
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        logging.info(f"Товар «{product.name}» добавлен на склад. Количество: {product.quantity}, цена: {product.price}.")

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                logging.info(f"Товар «{product.name}» удален со склада.")
                return

        logging.warning(f"Товар «{product_name}» на складе не найден.")

    def calc_total_cost(self):
        total_cost = sum(product.calc_total_cost() for product in self.products)
        logging.info(f"Общая стоимость всех товаров на складе: {total_cost} units")

        return total_cost


# Создаем сущности, добавляем товары, осуществляем покупки, формируем отчеты
jacket = Product("Куртка", 15, 6500)
coat = Product("Пальто", 10, 8000)

warehouse = Warehouse()
warehouse.add_product(coat)
warehouse.add_product(jacket)

seller = Seller("Иван Петров")
seller.sell_product(jacket, 3)
seller.sell_product(coat, 5)

print(seller.generate_sales_report())
print(f"На данный момент на складе товаров на общую сумму {warehouse.calc_total_cost()} units.")


```
