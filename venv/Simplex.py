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
    r = find_neg_bottom_row(table)
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
        n = find_neg_right_col(table)
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
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

def convert_min(table):
    table[-1,:-2] = [-1*i for i in table[-1,:-2]]
    table[-1,-1] = -1*table[-1,-1]
    return table

#returns the variables we need in terms of x1, x2, x3... according to the dimensions of the table
def gen_var(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x' + str(i+1))
    return v

#The user can't add too many constraints because we need at least one row of all zeros in the matricies to put the solution for all of the variables in
#so this method makes sure there are atleast two row of all zeros in the matricies before another constraint can be added.
def add_cons(table):
    lr = len(table[:,0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            total += j**2
            #I had to square it because if not then the values might just cancel each other out and appear as all zeros when they're not
        if total == 0:
            empty.append(total)
    if len(empty)>1:
        return True
    else:
        return False

#this function is taking the constraint and converting it into the appropriate format to be added into the matrix
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0,:])
        lr = len(table[:,0])
        var = lc - lr -1
        j = 0
        while j < lr:
            row_check = table[j,:]
            total = 0
            for i in row_check:
                total += float(i**2)
            if total == 0:
                row = row_check
                break
            j +=1
        eq = convert(eq)
        i = 0
        while i<len(eq)-1:
            row[i] = eq[i]
            i +=1
        row[-1] = eq[-1]
        row[var+j] = 1
    else:
        print('Cannot add another constraint.')

#I have to make sure that the last row in the matrix is empty, all zeros, so that I can add the objective function in the last row after all the constraints
def add_obj(table):
    lr = len(table[:,0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            total += j**2
        if total == 0:
            empty.append(total)
    if len(empty)==1:
        return True
    else:
        return False

#this actually adds the objective function if add_obj returns true
def obj(table,eq):
    if add_obj(table)==True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:,0])
        row = table[lr-1,:]
        i = 0
        while i<len(eq)-1:
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

#so this method is using the pivot methods to see if first more pivots are needed and if so it pivots around the identified element until there
#are no more negative elements in the last row or column, then it returns the max value of the objective function and all of the variables
def maxz(table):
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1,-1]
    return val

#this is the same as the maxz method excpt for a minimization problems
def minz(table):
    table = convert_min(table)
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
            val['min'] = table[-1,-1]*-1
    return val

#main method
if __name__ == "__main__":
    m = makeMatrix(2,2)
    constrain(m,'2,-1,G,10')
    constrain(m,'1,1,L,20')
    obj(m,'5,10,0')
    print(maxz(m))
