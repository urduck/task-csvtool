#!/bin/bash

# 1. Активация виртуального окружения, если оно есть
if [ -d "venv" ]; then
    echo "Активируем виртуальное окружение..."
    echo
    source venv/bin/activate
fi

# 2. Проверка наличия зависимостей
missing=0
python3 -c "import tabulate" 2>/dev/null || missing=1
python3 -c "import pytest" 2>/dev/null || missing=1

if [ $missing -eq 1 ]; then
    echo "Устанавливаем зависимости из requirements.txt..."
    echo
    pip install -r requirements.txt
fi

echo "Запускаем демонстрационные команды"
echo

# 3. Демонстрационные команды

# 1. Все товары Apple
echo '$ python3 main.py --file products.csv --where "brand=apple"'
python3 main.py --file products.csv --where "brand=apple"
echo

# 2. Товары с ценой выше 500
echo '$ python3 main.py --file products.csv --where "price>500"'
python3 main.py --file products.csv --where "price>500"
echo

# 3. Товары с рейтингом ниже 4.5
echo '$ python3 main.py --file products.csv --where "rating<4.5"'
python3 main.py --file products.csv --where "rating<4.5"
echo

# 4. Средняя цена всех товаров
echo '$ python3 main.py --file products.csv --aggregate "price=avg"'
python3 main.py --file products.csv --aggregate "price=avg"
echo

# 5. Максимальный рейтинг среди Samsung
echo '$ python3 main.py --file products.csv --where "brand=samsung" --aggregate "rating=max"'
python3 main.py --file products.csv --where "brand=samsung" --aggregate "rating=max"
echo

# 6. Минимальная цена среди Xiaomi
echo '$ python3 main.py --file products.csv --where "brand=xiaomi" --aggregate "price=min"'
python3 main.py --file products.csv --where "brand=xiaomi" --aggregate "price=min"
echo

# 7. Все товары с рейтингом 4.6 и выше
echo '$ python3 main.py --file products.csv --where "rating>4.5"'
python3 main.py --file products.csv --where "rating>4.5"
echo

# 8. Средний рейтинг среди товаров дешевле 500
echo '$ python3 main.py --file products.csv --where "price<500" --aggregate "rating=avg"'
python3 main.py --file products.csv --where "price<500" --aggregate "rating=avg"
echo

# 9. Товары с ценой от 200 до 800 (двойная фильтрация)
echo '$ python3 main.py --file products.csv --where "price>199"'
python3 main.py --file products.csv --where "price>199"
echo

echo '$ python3 main.py --file products.csv --where "price<801"'
python3 main.py --file products.csv --where "price<801"
echo

# 10. Фильтрация по несуществующему бренду (пограничный случай)
echo '$ python3 main.py --file products.csv --where "brand=sony"'
python3 main.py --file products.csv --where "brand=sony"
echo 