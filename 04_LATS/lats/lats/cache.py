from pathlib import Path
import pickle
import atexit


# Cache is a singleton class
# it has a dictionary of values
# data is stored in a pickle
# has getitem and setitem methods


class Cache:
    def __init__(self, cache_name=None):
        cache_name = cache_name or "cache"
        self.cache_fp = Path(__file__).parents[2] / f"{cache_name}.pickle"
        self.hits = 0

        self.data = {}
        if self.cache_fp.exists():
            self.load()
        atexit.register(self.save)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        values = self.data[key]
        if len(values) > 1:
            raise ValueError(f"Multiple values for key {key}")
        elif len(values) == 0:
            raise KeyError(key)
        else:
            self.hits += 1
            return values[0]

    def __setitem__(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)
        self.save()

    def __repr__(self):
        return f"Cache({len(self.data)} items)"

    def __str__(self):
        return f"Cache({len(self.data)} items)"

    def save(self):
        with self.cache_fp.open("wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        print(f'loading cache from {self.cache_fp}')
        with self.cache_fp.open("rb") as f:
            self.data = pickle.load(f)

    def items(self):
        return self.data.items()

cache = Cache()
