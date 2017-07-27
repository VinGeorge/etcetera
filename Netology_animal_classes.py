# Небольшая заготовка для ДЗ, с целью разобраться с понятием Class
# Просьба вернуть на доработку


class Animal:
    weigth = None
    current_speed = 0
    max_speed = 10
    flags = None

    def __init__(self, flags):
        self.flags = flags

    def voce(self):
        print("something")

    def start(self, value):
        self.current_speed += value

    def stop(self):
        self.current_speed = 0
        print('stopted')

animal = Animal("Yes")
print(animal.flags)
animal.voce()

class birds(Animal):
    max_speed = 20

Birds = birds('Yes')

print(Birds.__dict__)