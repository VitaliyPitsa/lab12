#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path


def get_train(trains, punkt_nazn, nomer, time):
    """
    Запросить данные о рейсе.
    """
    trains.append(
        {
            'punkt_nazn': punkt_nazn,
            'nomer': nomer,
            'time': time,
        }
    )
    return trains


def display_trains(trains):
    """
    Вывести данные о поездах.
    """
    # Проверить, что список поездов не пуст.
    if trains:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        # Заголовок таблицы.
        print(
            '| {:^30} | {:^20} | {:^20} |'.format(
                "Пункт назначиния",
                "Номер поезда",
                "время отправления"
            )
        )
        print(line)
        # Вывести данные о всех поездах.
        for idx, train in enumerate(trains, 1):
            print(
                '| {:<30} | {:<20} |  {:<20} |'.format(
                    train.get('punkt_nazn', ''),
                    train.get('nomer', ''),
                    train.get('time', '')
                )
            )
        print(line)


def select_train(trains, nomer):
    """
    Выбрать поезда с заданным типом.
    """
    # Сформировать список поездов.
    result = [train for train in trains if train.get('nomer', '') == nomer]
    # Возвратить список поездов.
    return result


def save_train(file_name, trains):
    """
    Сохранить все поезда в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(trains, fout, ensure_ascii=False, indent=4)


def load_train(file_name):
    """
    Загрузить все поезда из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
        return json.load(fin)


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select <номер> - запросить поезд по номеру;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


def main(command_line=None):
    """
    Главная функция программы.
    """
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления рейса.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new trains"
    )
    add.add_argument(
        "-p",
        "--punkt_nazn",
        action="store",
        required=True,
        help="The punkt_nazn name."
    )
    add.add_argument(
        "-n",
        "--nomer",
        action="store",
        type=int,
        help="The nomer of train."
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="The time."
    )

    # Создать субпарсер для отображения всех рейсов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all trains"
    )

    # Создать субпарсер для выбора рейса.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the train"
    )
    select.add_argument(
        "-no",
        "--nom",
        action="store",
        type=int,
        required=True,
        help="The nomer."
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все рейсы из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        trains = load_train(args.filename)
    else:
        trains = []

    # Добавить рейс.
    if args.command == "add":
        trains = get_train(
            trains,
            args.punkt_nazn,
            args.nomer,
            args.time
        )
        is_dirty = True

    # Отобразить всех рейсов.
    elif args.command == "display":
        display_trains(trains)

    # Выбрать требуемые самолеты.
    elif args.command == "select":
        selected = select_train(trains, args.nomer)
        display_trains(selected)

    # Сохранить данные в файл, если список рейсов был изменен.
    if is_dirty:
        save_train(args.filename, trains)


if __name__ == "__main__":
    main()