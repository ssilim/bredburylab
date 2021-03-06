"""
Есть два списка разной длины. 
В первом содержатся ключи, а во втором значения. 
Напишите код, который создаёт из этих ключей и значений словарь. 
Если ключу не хватило значения — в словаре должно быть значение None. 
Значения, которым не хватило ключей, нужно игнорировать.
На выходе скрипт. Язык: любой скриптовый.
"""

from itertools import zip_longest

key = ['k1', 'k2', 'k3']
value = ['v1', 'v2']
# value = ['v1', 'v2', 'v3', 'v4']

d = {k: v  for k, v in zip_longest(key, value) if k is not None}

print(d)
