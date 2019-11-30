# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
# you probably want to use this:
# import shop


def shop_loop(fruit: str):
    """
    Prints the same output as running `python shop.py` when called as "shop_loop('apples')".
    A for-loop is used for iterating over shops.
    This function does not have a returnvalue.
    :param fruit: (str) name of a fruit
    """
    shop_names = ['Aldi', 'Albert Heijn']
    shop_prices = [{'apples': 1.00, 'oranges': 1.50, 'pears': 1.75},
                   {'kiwis': 6.00, 'apples': 4.50, 'peaches': 8.75}]
    print(fruit)
    for x in range(len(shop_names)):
        print(f'Welcome to {shop_names[x]} fruit shop.')
        print(f'{fruit} cost {shop_prices[x]["apples"]} at {shop_names[x]}.')


if __name__ == '__main__':
    shop_loop('apples')
