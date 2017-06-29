def get_cook_book():
    with open ("2.1_cookbook.txt") as f:
        recipes = {}
        for line in f:
            dish = line.lower().strip()
            book = []
            for ing in range(int(f.readline())):
                ingridient = f.readline().split(" | ")
                inger = book.append({"ingridient_name": ingridient[0], "quantity": int(ingridient[1]), "measure": ingridient[2]})
            recipes[dish] = book
            f.readline()
        return recipes


def get_shop_list_by_dishes(dishes, person_count):
      shop_list = {}
      cook_book = recipes()
      for dish in dishes:
        for ingridient in cook_book[dish]:
          new_shop_list_item = dict(ingridient)

          new_shop_list_item['quantity'] *= person_count
          if new_shop_list_item['ingridient_name'] not in shop_list:
            shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
          else:
            shop_list[new_shop_list_item['ingridient_name']]['quantity'] +=
              new_shop_list_item['quantity']
      return shop_list

    def print_shop_list(shop_list):
      for shop_list_item in shop_list.values():
        print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'], 
                                shop_list_item['measure']))

    def create_shop_list():
      person_count = int(input('Введите количество человек: '))
      dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
        .lower().split(', ')
      shop_list = get_shop_list_by_dishes(dishes, person_count)
      print_shop_list(shop_list)

    create_shop_list()