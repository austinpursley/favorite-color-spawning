# color_evolution_v5.py
# Austin Pursley
# 5/6/2017
# The use of evolvetools for use with colors.

import evolvetools as et
import itertools
import random
import math


class Palette:
    # class for color values and functions to change those values.
    def __init__(self):
        self.num_colors = 0
        self.palette = []
        self.rgb_palette = []

    def set_num_colors(self, num_colors):
        self.num_colors = num_colors

    def create_palette_rand(self, num_colors):
        self.rgb_palette.clear()
        self.num_colors = num_colors
        for i in range(0, self.num_colors):
            self.rgb_palette.append([])
            for j in range(0, 3):
                 self.rgb_palette[i].append(random.randint(0,255))
            self.palette.append("#%02x%02x%02x" % ((self.rgb_palette[i])[0],
                                                   (self.rgb_palette[i])[1],
                                                   (self.rgb_palette[i])[2]))

def rgb_child(rgb_parent1, rgb_parent2, mutate=0):
    """
    From two parents color values, make child color.

    :param rgb_parent1: List of int values corresponding to RGB colors.
    :param rgb_parent2: Second list of RGB colors.
    :param mutate: Optional probability value for if bit will mutate.
    :return: a RGB color list with bits from both parents.
    """
    rgb_color = [0, 0, 0]
    for j in range(0, 3):
        rgb_color[j] = et.offspring(rgb_parent1[j], rgb_parent2[j],mutate)
    return rgb_color

def palette_child(parent1, parent2, mutate = 0):
    """
    Palete is list of colors. From two palettes, make similar child palette.
    :param parent1: A list of RGB colors.
    :param parent2: A list of RGB colors.
    :param mutate: Optional probability value for if bit will mutate.
    :return: A palette with bits from from both parents.
    """
    plte_child = Palette()
    plte_child.num_colors = parent1.num_colors
    for i in range(plte_child.num_colors):
        mom = parent1.rgb_palette[i]
        dad = parent2.rgb_palette[i]
        child = rgb_child(mom, dad, mutate)
        plte_child.rgb_palette.append(child)
        plte_child.palette.append("#%02x%02x%02x"%(child[0],child[1],child[2]))
    return(plte_child)

def palette_child_comb(parents,min_ospring_num, mutate = 0):
    """
    Return a child for all combination of parents from a list of parents.
    :param parents: list of parents.
    :param min_ospring_num: A minimum number of children to make.
    :param mutate: Optional probability value for if bit will mutate.
    :return: A list of children made from parents.
    """
    palette_child_list = []
    L = len(parents)
    parent_pair_num = int(math.factorial(L)/math.factorial(L-2))
    opp = int(round(min_ospring_num / parent_pair_num)) + 1
    for p in itertools.permutations(parents, 2):
        mom = p[0]
        dad = p[1]
        for i in range(opp):
            palette_child_list.append(palette_child(mom, dad, mutate))
    return palette_child_list