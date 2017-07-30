class Animals:
    current_speed_run = 0
    current_speed_fly = 0
    flags = None
    avr_weight = 50
    avr_height = 30
    get_voice = None

    def __init__(self, avr_weight, avr_height, flags, get_voice):
        self.avr_weight = avr_weight
        self.avr_height = avr_height
        self.get_voice = get_voice
        self.flags = flags

    def voice(self):
        print(self.get_voice)

    def running(self, value):
        self.current_speed_run += value

    def flying(self, value):
        if can_fly == "Yes":
            self.current_speed_fly += value
        else:
            print("It's mammals or chiken :( ")

    def sleep(self):
        self.current_speed_run = 0
        self.current_speed_fly = 0
        print("It's already asleep" )

    def stop(self):
        self.current_speed = 0
        print('stopted')


class Cows(Animals):
    avr_milk_daily = 10
    avr_speed_weight_month = 15
cows = Cows(150, 150, None, "МУУУ!")


class Goats(Animals):
    avr_milk_daily = 10
goats = Goats(40, 60, None, "Мееее!")

class Sheeps(Animals):
    avr_hair_month = 14
sheeps = Sheeps(40, 60, None, "Бееее!")

class Pigs(Animals):
    avr_speed_weight_month = 7

class Ducks(Animals):
    can_fly = "Yes"
    avr_duckling_season = 8

class Chikens(Animals):
    avr_eggs_daily = 2

class Gooses(Animals):
    Ga_ga = "Ofcourse"

cows.voice()