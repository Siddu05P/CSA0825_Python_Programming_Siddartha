import time, sys
from functools import lru_cache


print("\n=== Q5 Defaults ===")
def add_item_buggy(item, order=[]):
    order.append(item); return order
def add_item(item, order=None):
    if order is None: order = []
    order.append(item); return order
print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print(add_item_buggy.__defaults__)
def total_gst(price, rate=0.05): return price*(1+rate), price*rate
print(total_gst(100), total_gst(100, rate=0.18))
x = "global"
def f_local():
    x = "local"; return x
def f_global():
    global x; x = "changed"
def counter():
    n = 0
    def inc():
        nonlocal n; n += 1; return n
    return inc
f_local(); print(x); f_global(); print(x)
c = counter(); print(c(), c(), c())
def make_order():
    order = []
    def add(item): order.append(item); return list(order)
    return add
c1, c2, c3 = make_order(), make_order(), make_order()
print(c1("Tea"), c2("Vada"), c3("Dosa"), c1("Coffee"))

