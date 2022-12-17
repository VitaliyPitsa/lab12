#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os


def get_train(trains, name, no, time):
    """
        Запросить данные о рейсе.
        """
    trains.append(
        {
            'name': name,
            'no': no,
            'time': time,
        }
    )
    return trains


def display_trains(trains):
    if trains:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^30} | {:^20} | {:^20} |'.format(
                "Пункт назначиния",
                "Номер поезда",
                "время отправления"
            )
        )
        print(line)
        for idx, train in enumerate(trains, 1):
            print(
                '| {:<30} | {:<20} |  {:<20} |'.format(
                    train.get('name', ''),
                    train.get('no', ''),
                    train.get('time', '')
                )
            )
        print(line)


def select_poezd(trains, no):
    result = [train for train in trains if train.get('no', '') == no]
    return result


def save_poezd(file_name, trains):
    """
    Сохранить все поезда в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(trains, fout, ensure_ascii=False, indent=4)


def load_poezd(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
    return loadfile


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select <номер> - запросить поезд по номеру;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


@click.command()
@click.option("-c", "--command")
@click.argument("file_name")
@click.option("-n", "--name")
@click.option("-o", "--no", type=int)
@click.option("-t", "time")
def main(command, name, no, time, file_name):
    is_dirty = False
    if os.path.exists(file_name):
        trains = load_poezd(file_name)
    else:
        trains = []
    # Добавить поезд.
    if command == "add":
        staff = get_train(trains, name, no, time)
        is_dirty = True

    # Отобразить все поезда.
    elif command == "display":
        display_trains(trains)

    # Выбрать требуемый поезд.
    elif command == "select":
        selected = select_poezd(trains, no)
        display_trains(selected)

    # Сохранить данные в файл, если список поездов был изменен.
    if is_dirty:
        save_poezd(file_name, trains)


if __name__ == "__main__":
    main()