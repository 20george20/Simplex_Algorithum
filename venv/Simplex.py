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

"""this method finds our first pivot point. First it looks to see if there are any negative numbers in the last column
if there are then it finds the most negative value in the correspoinding row. Then, in the column corresponding to the
most negative number it finds the smallest ratio between the element in the column and its correspoinding element in the
last column. total is the list of all of these ratios and the smallest entry in total is our first pivot point."""
def loc_piv_r(table):
    total = []
    r = find_neg_r(table)
    row = table[r,:-1]
    m = min(row)
    c = np.where(row == m)[0][0]
    col = table[:-1,c]
    for i, b in zip(col,table[:-1,-1]):
        if i**2>0 and b/i>0:
            total.append(b/i)
        else:
            total.append(10000)
    index = total.index(min(total))
    return [index,c]

#this method is also finding a pivot point, but instead of finding it for a negative value in the last column, it finds
#a pivot point corresponing to a negative value in the last row
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i,b in zip(table[:-1,n],table[:-1,-1]):
            if b/i >0 and i**2>0:
                total.append(b/i)
            else:
                total.append(10000)
        index = total.index(min(total))
        return [index,n]

#this function pivots around an element in order to get rid of the negative in the last row or column
def pivot(row,col,table):
    lr = len(table[:,0])
    lc = len(table[0,:])
    t = np.zeros((lr,lc))
    pr = table[row,:]
    if table[row,col]**2>0:
        e = 1/table[row,col]
        r = pr*e
        for i in range(len(table[:,col])):
            k = table[i,:]
            c = table[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

"""this method is going to take the input we get from the user about an inequality and turn it into a form
my code will understand
eq is the inequiality, L is less than, G is greater than
an example input might be 1,3,4,L,6 --> 1x + 3y + 4z <= 6w """
def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        for i in eq:
            eq = float(i)*-1
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        for i in eq:
            eq = float(i)
        return eq