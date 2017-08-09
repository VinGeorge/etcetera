class Animals:
    current_speed_run = 0
    current_speed_fly = 0
    flags = None
    avr_weight = 50
    avr_height = 30
    get_voice = None

    def __init__(self, avr_weight, avr_height, get_voice, flags = None):
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


class Cow(Animals):
    avr_milk_daily = 10
    avr_speed_weight_month = 15
cow = Cow(150, 150, None, "МУУУ!")


class Goat(Animals):
    avr_milk_daily = 10
goat = Goat(40, 60, None, "Мееее!")

class Sheep(Animals):
    avr_hair_month = 14
sheep = Sheep(40, 60, None, "Бееее!")

class Pig(Animals):
    avr_speed_weight_month = 7

class Duck(Animals):
    can_fly = "Yes"
    avr_duckling_season = 8

class Chiken(Animals):
    avr_eggs_daily = 2

class Goos(Animals):
    Ga_ga = "Ofcourse"

cow.voice()

