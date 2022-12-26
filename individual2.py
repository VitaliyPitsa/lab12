#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json


@click.group()
def cli():
    pass


@cli.command("add")
@click.argument('file_name')
@click.option("-n", "--name")
@click.option("-o", "--no", type=int)
@click.option("-t", "time")
def get_train(file_name, name, no, time):
    """
        Запросить данные о рейсе.
        """
    trains = load_poezd(file_name)
    trains.append(
        {
            'name': name,
            'no': no,
            'time': time,
        }
    )
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(trains, fout, ensure_ascii=False, indent=4)
    click.secho("Поезд добавлен")


@cli.command("display")
@click.argument('file_name')
@click.option('--select', '-s', type=int)
def display_trains(file_name, select):
    """
        Вывести данные о поездах.
        """
    print(select)
    trains = load_poezd(file_name)

    if select == 1:
        trains = select_poezd(trains)

    line = '+-{}-+-{}-+-{}-+'.format(
        '-' * 30,
        '-' * 20,
        '-' * 20
    )
    # Заголовок таблицы.
    print(line)
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
                train.get('name', ''),
                train.get('no', ''),
                train.get('time', '')
            )
        )
    print(line)


def select_poezd(trains, no):
    """
        Выбрать поезда с заданным типом.
        """
    # Сформировать список поездов.
    result = [train for train in trains if train.get('no', '') == no]
    # Возвратить список поездов.
    return result


def load_poezd(file_name):
    """
    Загрузить все поезда из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
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


if __name__ == "__main__":
    cli()