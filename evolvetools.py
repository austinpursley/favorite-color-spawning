# color_evolution_v5.py
# Austin Pursley
# 5/6/2017
# Set of simple tools for implementing something like a genetic algorithm.

import random

# Operations for genetic algorithm computations.

def ith_bit(x, i):
    """
    Set the ith bit to x.
    """
    ith_bit = (x >> i) & 1
    return ith_bit

def set_ith_bit(x, y, i):
    """
    Set the ith bit of x to y
    """
    y ^= (-x ^ y) & (1 << i)
    return y

def crossover(p1, p2):
    """
    Form offspring from bit crossover of ints parent 1 and parent 2.

    :param: p1 parent 1, an int value
    :param: p2 parent 2, an int value
    :return: int value with half of bits from parents 1, other from parent 2.
    """
    # Initilize offspring to 0 for set_it_bit function below.
    offspring = 0
    # This is the probability of crossover.
    probability = 0.5
    # The length will be set to length of the largest number.
    if p1 > p2:
        length = len(bin(p1)) - 2
    else:
        length = len(bin(p2)) - 2
    # The crossover function loop
    for i in range(0, length):
        x = random.random()
        # Offspring gets ith bit from p1 if X > probability.
        if x > probability:
            # Set ib to ith bit in p1.
            ib = ith_bit(p1, i)
        else:
            # Set ib to ith bit in p2.
            ib = ith_bit(p2, i)
        # Set ith bit of offspring to ib.
        offspring = set_ith_bit(ib, offspring, i)
    return (offspring)

def mutation(individual, set_mutate=0):
    """
    Output a mutated input, where each bit has a chance of being switched.

    :param individual: int value
    :return: input value that has 0 or more bits toggled.
    """
    # bin(num) is a bit string, which looks like 0bXXXX, so we subtract 2.
    length = len(bin(individual)) - 2
    if set_mutate == 0:
        p = 1 / length
    elif set_mutate <= 1:
        p = set_mutate
    else:
        print("error: mutation probability greater than 1")
    # Loop through the bit string.
    for i in range(0, length):
        x = random.random()
        # Probability of mutation is 1 / length.
        if x < p:
            individual ^= 1 << i  #bit toggle
    return individual

def offspring(p1, p2, set_mutate=0):
    """
    Output an offspring int value from mutation and crossover of parent values.

    :param p1: parent 1, int value
    :param p2: parent 2, int value
    :return: offspring, created from crossover and mutation functions.
    """
    offspring = crossover(p1, p2)
    offspring = mutation(offspring,set_mutate)
    return offspring