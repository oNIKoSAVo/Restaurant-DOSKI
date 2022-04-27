from restaurant.models import MenueInRestaraunt


def has_category_dishes(category):
    return not len(category.menues_in_rastaraunt) == 0


def filter_categories(categories, restaurant):
    for category in categories:
        setattr(category, 'menues_in_rastaraunt',
                MenueInRestaraunt.objects \
                    .filter(menue__category=category, restaraunt=restaurant) \
                    .order_by('menue__dish'))
        print('category', category.__dict__)
        filtered_dishes = []
        for dish in category.menues_in_rastaraunt:
            if not dish.price == 9.223372036854776e+16:
                filtered_dishes.append(dish)
                dish.price = int(dish.price)
#                 print(dish.__dict__)
        category.menues_in_rastaraunt = filtered_dishes
    return list(filter(has_category_dishes, categories))
