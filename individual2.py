#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json


def get_train(train_load, name, no, time, file_name):
    train_load.append({"name": name, "no": no, "time": time})
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(train_load, fout, ensure_ascii=False, indent=4)
    return load_poezd(file_name)


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
@click.option("-o", "--no")
@click.option("-t", "time")
def main(command, name, no, time, file_name):
    poezd_load = load_poezd(file_name)
    if command == "add":
        get_train(poezd_load, name, no, time, file_name)
        click.secho("Данные добавлены")
    elif command == "display":
        list(poezd_load)
    elif command == "select":
        select_poezd(poezd_load)


if __name__ == "__main__":
    main()