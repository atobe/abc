# simple k-v cache in a pickle
from pathlib import Path
import pickle


class Cache:
    CACHE_PATH = Path(__file__).parent / "cache.pickle"

    def __init__(self, path=None):
        self.path = path or Path(self.CACHE_PATH)
        self.data = self.load()

    def load(self):
        if self.path.exists():
            with self.path.open("rb") as f:
                return pickle.load(f)
        return {}

    def save(self):
        # ensure directory path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("wb") as f:
            pickle.dump(self.data, f)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if key not in self.data:
            print(f"saving new key: {key}")
        self.data[key] = value
        self.save()

    def __contains__(self, key):
        return key in self.data

    def __delitem__(self, key):
        del self.data[key]
        self.save()
        
    def keys(self):
        return self.data.keys()


cache = Cache()


def cached_or_not(key, func, *args, **kwargs):
    if key in cache:
        return cache[key]
    result = func(*args, **kwargs)
    cache[key] = result
    return result
