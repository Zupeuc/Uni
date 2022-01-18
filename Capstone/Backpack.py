from sys import stdin
from sys import stdout

'''
Knapsack Problem implementation

Created on Dec 6, 2010
@author: rohanbk
'''
capacity = 5
num_of_items = 6
total_weight = 0
total_value = 0

# Initialize backpack
B = [[0] * (capacity + 1) for i in range(num_of_items)]
# Keep list will help determine which items to keep once we've solved the Knapsack problem
keep = [[0] * (capacity + 1) for i in range(num_of_items)]


# Dictionary to store item numbers and corresponding weights
# <Item number, weight>
#aca podria cambiar el codigo o numero del producto
item_weight = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
# Dictionary to store item numbers and corresponding values
# <Item number, value>
item_value = {0: 10, 1: 1, 2: 2, 3: 0, 4: 30, 5: 100}


#____________________________________INPUT DEL CLASSIFICATION AREA
lista1 = ["B1","B1","B1","B1","B1"]
n_track1 = len(lista1)
item_weight[0] = n_track1
valor_original = item_value[0]
print("%%%%%%%%%%%")
print(valor_original)
item_value[0] = valor_original*n_track1
print(item_value[0])
print("$$$$$$$$$$$$$")

lista2 = ["B2","B2","B2"]
n_track2 = len(lista2)
item_weight[1] = n_track2
valor_original = item_value[1]
item_value[1] = valor_original*n_track2

lista3 = ["B3", "B3"]
n_track3 = len(lista3)
item_weight[2] = n_track3
valor_original = item_value[2]
item_value[2] = valor_original*n_track3

lista4 = ["B4", "B4"]
n_track4 = len(lista4)
item_weight[3] = n_track4
valor_original = item_value[3]
item_value[3] = valor_original*n_track4

lista5 = ["B5", "B5"]
n_track5 = len(lista5)
item_weight[4] = n_track5
valor_original = item_value[4]
item_value[4] = valor_original*n_track5

lista6 = ["B6"]
n_track6 = len(lista6)
item_weight[5] = n_track6
valor_original = item_value[5]
item_value[5] = valor_original*n_track6

if n_track1 + n_track2 < 30:
    pass
    #no puedo tren tipo 1
    #return False

#-------------------------------------------------------------------------ARMAR EL TREN

total_weight = sum([value for value in item_weight.values()])
total_value = sum([value for value in item_value.values()])

# Solve Knapsack problem
for k in range(num_of_items):
    for w in range(capacity + 1):
        if w >= item_weight[k]:
            #si el n capacidad es mayor que el peso del producto k
            p1 = B[k - 1][w] #peso que ya hay en la mochila
            p2 = B[k - 1][w - item_weight[k]] + item_value[k] #valor del producto a decidir si entrar o no, utilidad
            print("el n de capacidad es mayor que el peso del producto k")
            print(w)
            print(k)
            print(B[k-1]) #si k es 0 es el ultimo valor de la lista B
            print("-------")
            if p1 > p2:
                keep[k][w] = 0
                B[k][w] = p1
            else:
                keep[k][w] = 1
                B[k][w] = p2
        else:
            print("el n de capac no es mayor que el peso del producto k")
            print(w)
            print(k)
            B[k][w] = B[k - 1][w]
            keep[k][w] = 0
        print(B)
        print(keep)

rem_capacity = capacity
items_to_take = []
valueofgoods = 0

# Determine which items to keep and what their total value is
for k in range(num_of_items - 1, -1, -1):
    print("")
    print("")
    print(k)
    if keep[k][rem_capacity] == 1:
        print("entro")
        items_to_take.append(k)
        rem_capacity = rem_capacity - item_weight[k]
        valueofgoods += item_value[k]
       # keep.pop(k)
print('Total value of all goods: %s' % (total_value))
print('Goods to choose: %s' % (items_to_take))
print('Maximized Value of goods: %s' % (valueofgoods))
print('Opportunity cost: %s' % (total_value - valueofgoods))

for i in range(len(items_to_take)):
    items_to_take[i] += 1
print(items_to_take)

print('Lineas del track que pullbakié: %s' % (items_to_take))