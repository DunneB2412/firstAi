# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
import shop  # contains FruitShop class definition


def shop_smart(order: list, shops: list) -> shop.FruitShop:
    index = 0
    endPrices = [0.0, 0.0]
    for shop in shops:
        for fruit in order:
            if fruit[0] in shop.prices:
                endPrices[index] += shop.prices.get(fruit[0])*fruit[1]
        index += 1

    best = shops[0]
    if endPrices[1] < endPrices[0]:
        best = shops[1]
    """
    Calculate at which shop the given order is cheapest.
    :param order: (list) a list of (fruit, amount) tuples
    :param shops: (list) a list of FruitShops
    :returns: (shop.FruitShop) the shop that at which the order is cheapest
    """
    return best


def main():
    fruits1 = {'apples': 2.0, 'oranges': 1.0}
    fruits2 = {'apples': 1.0, 'oranges': 5.0}
    shop1 = shop.FruitShop('shop1', fruits1)
    shop2 = shop.FruitShop('shop2', fruits2)
    shops = [shop1, shop2]
    order1 = [('apples', 1.0), ('oranges', 3.0)]
    order2 = [('apples', 3.0)]
    print(f'For order {order1} the best shop is {shop_smart(order1, shops).name}.')
    print(f'For order {order2} the best shop is {shop_smart(order2, shops).name}.')


if __name__ == '__main__':
    main()
