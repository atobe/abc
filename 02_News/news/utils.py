import pickle

def rp(fp):
    with open(fp, "rb") as f:
        return pickle.load(f)


def wp(obj, fp):
    with open(fp, "wb") as f:
        pickle.dump(obj, f)


