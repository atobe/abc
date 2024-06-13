import hashlib

def phrase(parts):
    return " ".join([part.strip('"').strip("'") for part in parts])


def hashstring(s):
    return hashlib.md5(s.encode()).hexdigest()
