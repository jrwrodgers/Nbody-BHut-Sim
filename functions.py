def addM(a, b):
    res = []
    for i in range(len(a)):
        res.append(a[i]+b[i])
    return res

def multMs(a, b):
    res = []
    for i in range(len(a)):
        res.append(a[i]*b)
    return res

def print_attrs(a):
    attrs = vars(a)
    print(', '.join("%s: %s" % item for item in attrs.items()))