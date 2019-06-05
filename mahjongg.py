
'''
read mahjong tiles and decide which to throw and win in least amount of hands！

@author     Qida
'''

import csv
from itertools import groupby
from operator import itemgetter

# ---------------------------- -----------------------------


def check_three(tile):
    """ #return all three same tiles found 
        such as (1B1B1B)
        Arguments: All tiles in hand
    """
    Number_three = 0
    results = []
    temp = []

    for j in range(len(tile)):
        count = 0
        for i in range(len(tile)):
            if (tile[i] == tile[j] and i != j):
                count += 1
        if (count >= 2):
            temp.append(tile[j])
            temp.append(tile[j])
            temp.append(tile[j])
            Number_three += 1
            break
    if(temp != []):
        results.append(temp)

    return results

# ---------------------------------------------------------


def check_runs(tile):
    """ #return all runs of three tiles found  such as (1B2B3B)
        Arguments: All tiles in hand
    """
    results = []
    for j in tile:
        threesame = j
        for i in tile:
            num_runs = ''
            if(int(i[0]) == int(threesame[0])+1
               and i[1] != threesame[1]):
                num_runs = i
                results = ''
                for k in tile:
                    if(int(k[0]) == int(num_runs[0])+1 and
                       k[1] != num_runs[1]
                       and k[1] != threesame[1]):
                        results = k
                        results.append([threesame,
                                        num_runs, results])

    return results

# ---------------------------------------------------------


def check_pair(tile):
     """ #return all pairs found  such as (1B1B)
        Arguments: All tiles in hand
    """

    results = []
    for j in range(len(tile)):
        for i in range(len(tile)):
            if(tile[i] == tile[j] and i != j):
                results.append(tile[j])
                results.append(tile[j])
                return results


# ---------------------------------------------------------


Tile_sequence = []
hands = 1

# Read tile sequence from csv file 
with open('dealsequence.csv') as s:
    reader = csv.reader(s)
    Tile_sequence = list(reader)
tile = []
win = 0
for i in range(136):
    tile.append(Tile_sequence[0][0])
    Tile_sequence.pop(0)
    Tile_sequence.append(tile[0])
    tile.pop(0)
for i in range(13):
    tile.append(Tile_sequence[0])
    Tile_sequence.pop(0)

win = 0
while(win == 0):
    print("Hands:", hands)

    tile.append(Tile_sequence[0])  # take a new tile
    Tile_sequence.pop(0)
    print("New tile:", tile[-1])
    tile.sort()
    print("New Set:")
    print(tile)

    tile = []
    C = []
    W = []# wind
    D = []# dragon
    X = []

  # categorize tiles 
    for i in tile:
        if(i[1] == 'tile'):
            tile.append(i)
        elif(i[1] == 'C'):
            C.append(i)
        elif(i[1] == 'W'):
            W.append(i)
        elif(i[1] == 'D'):
            D.append(i)
        else:
            X.append(i)

    C.sort()
    tile.sort()
    W.sort()



    # find 3 same tiles
    Number_three = []

    Number_three = check_three(tile)+check_three(C)+check_three(W)
    if (len(D) >= 3):
        Number_three.append([D[0], D[1], D[2]])
        D.pop()
        D.pop()
        D.pop()
    if (len(X) >= 3):
        Number_three.append([X[0], X[1], X[2]])
        X.pop()
        X.pop()
        X.pop()

    threesame = len(Number_three)

    print("3 of a kind:", Number_three)

    # find runs of 3
    num_runs = 0
    tile_C_W = []
    tile_C_W.extend(C)
    tile_C_W.extend(W)
    tile_C_W.extend(tile)

    tile_C_W.sort()
    for j in Number_three:
        for i in j:
            for k in range(len(tile_C_W)):
                if(tile_C_W[k] == i):
                    tile_C_W.pop(k)
                    break

    C_W_runs = check_runs(tile_C_W)
    runs = []

    for j in range(len(C_W_runs)):
        if(all(x in tile_C_W for
               x in C_W_runs[j])):
            runs.append(C_W_runs[j])
            for i in C_W_runs[j]:
                for k in range(len(tile_C_W)):
                    if(tile_C_W[k] == i):
                        tile_C_W.pop(k)
                        break

    print("runs of 3:  ", runs)

    num_runs = len(runs)

    # find pairs
    pairs = 0
    flag = 0
    results = []
    D = [x for x in D if x not in Number_three]
    X = [x for x in X if x not in Number_three]
    if (len(D) > 1):
        flag = 1
        for i in range(2):
            pairs.append(D[i])
    elif (flag == 0 and len(X) > 1):
        flag = 1
        for i in range(2):
            pairs.append(X[i])

    else:
        pairs = check_pair(tile_C_W)
    print("pairs:       ", pairs)

    num_pairs = int(len(pairs)/2)
    print("Total #: 3 of a kind:", threesame,
          "; runs of 3:", num_runs, "; pairs:",  num_pairs)
    if(threesame+num_runs == 4 and num_pairs == 1):
        print("You win!!!!")
        win = 1
    else:
        print("No winning hand...")
        hands += 1
        for i in range(len(tile)-1, 0, -1):
            if (tile[i] not in Number_three and tile[i] not in C_W_runs and
                    tile[i] not in pairs):
                print("Discard tile:", tile[i])
                tile.pop(i)
                break

    tile.sort()

    print("==========================")
