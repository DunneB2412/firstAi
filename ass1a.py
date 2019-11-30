# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions

fruit_prices = {'apples': 2.00,
                'oranges': 1.50,
                'pears': 1.75,
                'limes': 0.75,
                'strawberries': 1.00}


def order_price(order: list) -> float:
    price=0
    for i in order:
        #print(i)
        if i[0]in fruit_prices:
            for ii in range(i[1]):
                price+=fruit_prices[i[0]]
        else:
            return None
    """
    Calculate the total price of the order (the sum of the price of each fruit in the order times its amount).
    If any fruit in the order is not in store return None, else return the total price as a real.
    :param order: (list) a list of (fruit, amount) tuples
    :returns: (float) total price unless input invalid then None
    """
    return price


"""
BONUS ASSIGNMENT
"""
def quicksort(lst: list) -> list:
    lst.sort()
    """
    Sort the input list in non-decreasing order by quicksort.
    :param lst: (list) a list of items that have an inherent order (numbers, strings etc.)
    :returns: (list) an ordered version of the input list
    """
    raise lst


if __name__ == '__main__':
    order1 = [('apples', 2), ('pears', 3), ('limes', 4)]
    print(f'Cost of {order1} is {order_price(order1)}')

    order2 = [('pears', 2), ('limes', 1), ('strawberries', 10), ('melons', 3)]
    print(f'Cost of {order2} is {order_price(order2)}')
