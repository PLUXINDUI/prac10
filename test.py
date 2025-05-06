import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Установка seed для воспроизводимости результатов
np.random.seed(42)
random.seed(42)

# Определяем количество строк
num_rows = 100

# Создаем словарь для хранения данных
data = {}

# Числовые данные
data['Продажи'] = np.random.normal(1000, 200, num_rows).round(2)
data['Маржа'] = np.random.uniform(0.05, 0.25, num_rows).round(4)
data['Количество'] = np.random.randint(1, 100, num_rows)
data['Цена'] = (data['Продажи'] / data['Количество']).round(2)

# Дата
start_date = datetime(2023, 1, 1)
data['Дата'] = [start_date + timedelta(days=random.randint(0, 365)) for _ in range(num_rows)]

# Категориальные данные
categories = ['Электроника', 'Одежда', 'Книги', 'Товары для дома', 'Спорт', 'Продукты']
data['Категория'] = [random.choice(categories) for _ in range(num_rows)]

customer_types = ['Розница', 'Опт', 'Онлайн']
data['ТипКлиента'] = [random.choice(customer_types) for _ in range(num_rows)]

regions = ['Север', 'Юг', 'Восток', 'Запад', 'Центр']
data['Регион'] = [random.choice(regions) for _ in range(num_rows)]

# Добавляем числовой столбец с пропущенными значениями
data['Рейтинг'] = np.random.uniform(1, 5, num_rows).round(1)
# Добавляем пропущенные значения (примерно 10%)
missing_indices = np.random.choice(num_rows, size=int(num_rows * 0.1), replace=False)
for idx in missing_indices:
    data['Рейтинг'][idx] = np.nan

# Добавляем категориальный столбец с пропущенными значениями
data['СпособОплаты'] = [random.choice(['Карта', 'Наличные', 'Банковский перевод', 'PayPal']) for _ in range(num_rows)]
# Добавляем пропущенные значения (примерно 15%)
missing_indices = np.random.choice(num_rows, size=int(num_rows * 0.15), replace=False)
for idx in missing_indices:
    data['СпособОплаты'][idx] = None

# Добавляем бинарные данные
data['Возврат'] = [random.choice([0, 1]) for _ in range(num_rows)]
data['СрочныйЗаказ'] = [random.choice([0, 1]) for _ in range(num_rows)]

# Создаем DataFrame из словаря
df = pd.DataFrame(data)

# Сохраняем как Excel файл
df.to_excel('test_data.xlsx', index=False)

print("Тестовый Excel-файл 'test_data.xlsx' успешно создан.")