# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json.

import json
import datetime
from decimal import getcontext, Decimal
import re
from termcolor import cprint
import csv


class RpgGame:

    def __init__(self):
        self.remaining_time = '123456.0987654321'
        self.time = Decimal(0)
        self.experience = 0
        self.mobs = []
        self.travel_location = []
        self.location_object = []
        self.location_name = []
        self.exp_tm = r'\d+'
        self.tm = r"tm(\d.+)"
        self.float_count = getcontext().prec = 20
        self.exp_to_travel = 280
        self.writer = None
        self.file = None
        self.field_names = ['current_location', 'current_experience', 'current_date']
        self.result_game = []

    def create_file(self):
        with open('dungeon.csv', 'w', newline='') as out_txt:
            self.writer = csv.writer(out_txt)
            self.writer.writerow(self.field_names)

    def save_result(self):
        with open('dungeon.csv', 'a', newline='') as out_result:
            self.writer = csv.writer(out_result)
            self.result_game.extend([self.location_name[0], self.experience, datetime.datetime.now()])
            self.writer.writerow(self.result_game)

    def open_maps(self):
        with open('rpg.json', 'r') as rpg:
            self.file = json.load(rpg)
            self.location_object.extend(self.file['Location_0_tm0'])
            self.location_name.extend(self.file.keys())

    def create_location(self):
        for index, new_obj in enumerate(self.location_object):
            if isinstance(new_obj, str):
                self.mobs.append((index, new_obj))
            elif isinstance(new_obj, dict):
                names = list(new_obj.keys())[0]
                self.travel_location.append((index, names))

    def printing(self):
        cprint(f'Вы находитесь в {self.location_name[0]}\n'
               f'У вас {self.experience} опыта, осталось {datetime.timedelta(seconds=float(self.remaining_time))} до '
               f'наводнения\n'
               f'Прошло времени: {datetime.timedelta(seconds=float(self.time))}\n'
               f'Внутри вы видите: ', color='cyan')
        for mob in self.mobs:
            cprint(f'Монстра -- {mob[1]}', color="green")
        for lok in self.travel_location:
            cprint(f'Вход в локацию: {lok[1]}', color="yellow")
        print('Выберите действие:\n'
              '1.Атаковать монстра\n'
              '2.Перейти в другую локацию\n'
              '3.Сдаться и выйти из игры')

    def user_input(self):
        while True:
            self.printing()
            choice = input("Что же мы делаем?: ")
            if choice == '1':
                if not self.mobs:
                    cprint("Нет мостров для атаки", color='red')
                    continue
                else:
                    for count, monster in enumerate(self.mobs):
                        cprint(f"{count + 1}: {monster[1]}", color='green')
                    select = input("Выберете монстра для атаки: ")
                    if select.isalpha():
                        print("Вводи цифры, буквы не допустимы!!")
                        continue
                    elif int(select) > len(self.mobs):
                        print("Не правильно введено число!")
                        continue
                    else:
                        selects_mobs = self.mobs[int(select) - 1]
                        count_exp_tm = re.findall(self.exp_tm, selects_mobs[1])
                        self.experience += Decimal(str(count_exp_tm[0]))
                        self.time += int(count_exp_tm[1])
                        self.mobs.pop(int(select) - 1)
            elif choice == "2":
                if not self.travel_location:
                    if self.mobs:
                        continue
                    else:
                        return cprint("Мы попали в тупик.. прийдется начинать с начала...", color='red')
                else:
                    for count, lokationses in enumerate(self.travel_location):
                        cprint(f"{count + 1}: {lokationses[1]}", color='yellow')
                    choice_location = input(f'В какую локацию идем? \n')
                    if int(choice_location) > len(self.travel_location):
                        print("Не правильно введено число!")
                        continue
                    elif "Hatch" in self.travel_location[0][1]:
                        if self.experience < self.exp_to_travel:
                            return print("Слишком мало опыта для перехода в локацию...")
                        else:
                            return print("You are Winner!!!")
                    else:
                        your_choice = self.travel_location[int(choice_location) - 1]
                        count_lok_tm = re.findall(self.tm, your_choice[1])
                        self.time += Decimal(str(count_lok_tm[0]))
                        self.location_object = self.location_object[your_choice[0]][your_choice[1]]
                        self.mobs.clear()
                        self.travel_location.clear()
                        self.create_location()
                        self.location_name.append(your_choice[1])
                        self.location_name.pop(0)
                        self.save_result()
                        self.result_game.clear()

            elif choice == "3":
                return cprint("Беги глупец, ты огурец, на поле боя не желец!", color='red')
            elif not choice.isdigit() or not choice.isalpha():
                cprint('Ты что вводишь, цыфр не видишь?? Пробуй еще!', color='red')
                continue

    def run(self):
        self.create_file()
        self.open_maps()
        self.create_location()
        while True:
            self.user_input()
            game_of_white_thrones = input("Если ты хочешь продолжить введи yes, если ты хочешь выйти введи:q ")
            if game_of_white_thrones == "yes":
                continue
            elif game_of_white_thrones == "q":
                print("game Over")
                break


if __name__ == "__main__":
    game = RpgGame()
    game.run()