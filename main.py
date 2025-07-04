import argparse
import csv
from tabulate import tabulate
import re


def filter_rows(rows, column, operator, value):
    """
    Фильтрует строки по условию column operator value.
    Поддерживает >, <, = для числовых и строковых значений.
    """
    def op_func(v1, v2):
        if operator == '>':
            return v1 > v2
        elif operator == '<':
            return v1 < v2
        elif operator == '=':
            return v1 == v2
        else:
            raise ValueError(
                "Поддерживаются только операторы >, <, ="
            )

    def cast(val):
        try:
            return float(val)
        except ValueError:
            return val

    value = cast(value)
    return [row for row in rows if op_func(cast(row[column]), value)]


def aggregate_column(rows, column, func):
    """
    Агрегирует значения столбца column по функции func (avg, min, max).
    Работает только с числовыми значениями.
    """
    values = [float(row[column]) for row in rows]
    if func == "avg":
        return sum(values) / len(values)
    elif func == "min":
        return min(values)
    elif func == "max":
        return max(values)
    else:
        raise ValueError(
            "Агрегация поддерживает только: avg, min, max"
        )


def read_csv(file_path):
    """
    Читает CSV-файл и возвращает список словарей (строк).
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def print_table(rows, headers=None, colalign=None):
    """
    Форматированный вывод таблицы.
    """
    output = tabulate(rows, headers=headers, tablefmt="grid", colalign=colalign)
    output = output.replace('=', '-')
    lines = output.splitlines()
    new_lines = []
    hline_indices = [i for i, line in enumerate(lines) if set(line.strip()) <= {'+', '-'}]
    for i, line in enumerate(lines):
        if set(line.strip()) <= {'+', '-'}:
            if i in (hline_indices[0], hline_indices[1], hline_indices[-1]):
                new_lines.append(line)
        else:
            new_lines.append(line)
    print('\n'.join(new_lines))


def main():
    """
    Точка входа: парсит аргументы, читает файл, фильтрует, агрегирует и выводит результат.
    """
    parser = argparse.ArgumentParser(
        description="CSV фильтр и агрегатор"
    )
    parser.add_argument(
        "--file", required=True, help="Путь к CSV-файлу"
    )
    parser.add_argument(
        "--where",
        help="Фильтрация: column>value, column<value, column=value (например price>100)"
    )
    parser.add_argument(
        "--aggregate",
        help="Агрегация: column=func (например price=avg)"
    )
    args = parser.parse_args()

    rows = read_csv(args.file)

    if args.where:
        try:
            pattern = r"([\w_]+)\s*([<>=])\s*(.+)"
            m = re.match(pattern, args.where)
            if m:
                column, op, value = m.groups()
            elif '=' in args.where:
                column, condition = args.where.split("=")
                op, value = condition[0], condition[1:]
            else:
                raise ValueError(
                    "Некорректный формат фильтрации. Пример: rating>4.7 или price=>100"
                )
            rows = filter_rows(rows, column.strip(), op, value.strip())
        except Exception as e:
            print(f"Ошибка фильтрации: {e}")
            return

    if args.aggregate:
        try:
            col, func = args.aggregate.split("=")
            result = aggregate_column(rows, col.strip(), func.strip())
            formatted = f"{float(result):.2f}"
            print_table([[formatted]], headers=[func.strip()], colalign=("right",))
        except Exception as e:
            print(f"Ошибка агрегации: {e}")
    else:
        if rows:
            print_table(rows, headers="keys")
        else:
            print("Нет данных для отображения.")


if __name__ == "__main__":
    main()
