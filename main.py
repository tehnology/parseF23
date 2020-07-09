from pathlib import Path
import itertools
from itertools import combinations
import matplotlib.pyplot as plt

# file_name = Path(r'\\nts2dc\W1User\Ficep_2\11824_1-01.fnc')
# file_name = Path(r'\\nts2dc\W1User\Ficep_2\11815_1-01.fnc')
file_name = Path(r'\\nts2dc\W1User\Ficep_2\10181_1-01.fnc')
DELTA = 1000


def get_dct_holes(path):
    holes_dict = {}
    with open(path) as f:
        lines = f.readlines()  # list containing lines of file
        for line in lines:
            if '[HOL]' in line:
                line = line.strip('[HOL] ')
            line = line.strip()
            if 'TS33' in line:
                line = line.split()[1:]
                # print(line)
                dia = line[0][2:]
                x_coord = line[1][1:]
                y_coord = line[2][1:]

                if '.' in x_coord:
                    x_coord = float(x_coord)
                else:
                    x_coord = int(x_coord)
                if '.' in y_coord:
                    y_coord = float(y_coord)
                else:
                    y_coord = int(y_coord)

                if not holes_dict.get(dia):
                    holes_dict[dia] = {}

                if not holes_dict[dia].get(x_coord):
                    holes_dict[dia][x_coord] = []

                holes_dict[dia][x_coord].append(y_coord)
    return holes_dict


def count_holes(dct):
    otvet = {}
    for dia, dct_inner in dct.items():
        otvet[dia] = 0
        for item in dct_inner.values():
            otvet[dia] += len(item)
    return otvet


def num_of_pairs(lst):
    comb = set(combinations(lst, 2))
    comb_clean = set([i for i in comb if abs(float(i[0])-float(i[1])) > DELTA])
    # print(comb_clean)
    def check_isset(tpls):
        if len(tpls)*2 == len(set(itertools.chain.from_iterable(tpls))):
            return True
        else:
            return False

    i=0
    pairs = None
    while not pairs:
        num_of_pairs = (len(lst)// 2)-i
        comb_2 = set(combinations(comb_clean, num_of_pairs))
        i += 1
        #print('comb_2: ', comb_2)
        pairs = [c for c in comb_2 if check_isset(c)]
        # print(i)
        # if pairs:
        #     print('CO: ', pairs[0], sep="\n")
        #     print('Num_of_pairs: ', num_of_pairs)
        if pairs:
            print(pairs[0])
            print(num_of_pairs)
        #     coords = [item for sublist in pairs[0] for item in sublist]
                  # [item for sublist in l for item in sublist]
    # print(pairs)
    return num_of_pairs

def num_of_pairs_(lst):
    lst.sort()
    mid = len(lst) // 2
    lst1 = lst[:mid]
    lst2 = lst[-mid:]
    # print(lst1, lst2)

    res = []
    for num1 in lst1:
        for num2 in lst2:
            if abs(num1-num2) > DELTA:
                res.append((num1, num2))
                break
    if res:
        # print(len(res), res)
        return len(res)
    else:
        return 0


def split_dicts(dct_input):
    i = 0
    for dia, dct_inner in dct_input.items():
        for x_coord, y_list in dct_inner.items():
            if len(y_list)>1:
                if (len(y_list) == 2 and abs(float(y_list[0])-float(y_list[1]))>DELTA) or len(y_list)>2:
                    # print(len(y_list))
                    # print(y_list)
                    i += num_of_pairs_(y_list)
    return i

###

if __name__ == '__main__':

    dct_input = get_dct_holes(file_name)
    print(dct_input)
    summa_par = split_dicts(dct_input)
    print(count_holes(dct_input))
    print(summa_par)
    # print(dct_input)
    # print(count_holes(dct_input))
    # print(num_of_pairs(['2435', '2365', '2245', '2175', '2055', '1985', '1865', '1795', '1675', '1605', '1485', '1415']))

    # plt.axes()
    # def draw_circles(plt, dct_input, color=None):
    #
    #     for dia, dct_inner in dct_input.items():
    #         for x_coord, y_coord_list in dct_inner.items():
    #             for i in y_coord_list:
    #                 # print(x_coord, i)
    #                 circle = plt.Circle((float(x_coord), float(i)), radius=int(dia), fc=color, fill=False)
    #                 plt.gca().add_patch(circle)
    #     plt.axis('scaled')
    #
    # draw_circles(plt, dct_input, color='g')
    # plt.show()


