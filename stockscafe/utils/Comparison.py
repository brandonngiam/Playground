import numpy as np

def compareNumbers(alist, blist, epsilon, debug=False):
    if len(alist) != len(blist):
        return False
    for i in range(len(blist)):
        if debug:
            print(f'{alist[i]} vs {blist[i]}')
        if ((np.isnan(alist[i]) and np.isnan(blist[i])) or abs(alist[i] - blist[i]) <= epsilon) == False:
            return False    
    return True
