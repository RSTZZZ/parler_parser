def merge_two_dicts(x, y):
    '''
    Helper function to merge dictionary x and y.
    '''
    z = x.copy()
    z.update(y)
    return z
