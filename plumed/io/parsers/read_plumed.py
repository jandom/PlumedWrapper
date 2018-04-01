
def read_plumed(f):
    def foo(token): return float(token.split("=")[-1])
    line = [l for l in open(f).readlines() if "RESTRAINT" in l][-1]
    tokens = line.split()

    center = [token for token in tokens if token.startswith("AT")][-1]
    weight = [token for token in tokens if token.startswith("KAPPA")][-1]

    center, weight = foo(center), foo(weight)

    ind = int(f.split(".")[-2])
    return ind, center, weight
