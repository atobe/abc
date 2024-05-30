from pathlib import Path
import pickle

NEWS_DIR = Path(__file__).parents[1] / "data"


class FakeNewsAPI:
    def __init__(self):
        self.response_fps = self.load_responses()

    def load_responses(self):
        # data/20240512-091403.pickle
        # order them by datetime
        response_fps = list(NEWS_DIR.glob("*.pickle"))
        response_fps.sort()
        return response_fps

    def __iter__(self):
        return self

    def __next__(self):
        if not self.response_fps:
            raise StopIteration
        response_fp = self.response_fps.pop(0)
        response = pickle.loads(response_fp.read_bytes())
        return response

    def __getitem__(self, index):
        response_fp = self.response_fps[index]
        response = pickle.loads(response_fp.read_bytes())
        return response

def read_update_index(reset=False):
    index_fp = Path(__file__).parents[1] / "cache" / "fake_news_index.txt"
    index = next_index = int(index_fp.read_text().strip())
    if reset:
        next_index = 0
    else:
        next_index += 1
    index_fp.write_text(str(next_index) + "\n")
    return index

def reset():
    read_update_index(reset=True)

def get_latest_news():
    index = read_update_index()

    fn_api = FakeNewsAPI()
    return fn_api[index]

