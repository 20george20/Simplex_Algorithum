#this is a start to my simplex algorithum, I am trying to make it work for any amount of variables/constraints

import numpy as np


#making a matrix of constraints and variables (includes surplus, artificial, slack, and M variables.)
def makeMatrix(var, cons):
    matrix = np.zeros((cons + 1, var + cons + 2))
    return matrix
#making sure non of the constraints has a negative number
def next_round_r(table):
    m = min(table[:-1,-1])
    if m>= 0:
        return False
    else:
        return True
#this checks if there is a negative value in the objective equation (placed in lat row of matrix)
def next_round(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>=0:
        return False
    else:
        return True
#these two methods find the areas where the two boolean methods apply - aka where I will need to change the equations
def find_neg_right_col(table):
    lc = len(table[0,:])
    m = min(table[:-1,lc-1])
    if m<=0:
        n = np.where(table[:-1,lc-1] == m)[0][0]
    else:
        n = None
    return n
def find_neg_bottom_row(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m<=0:
        n = np.where(table[lr-1,:-1] == m)[0][0]
    else:
        n = None
    return n

