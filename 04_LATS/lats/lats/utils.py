# e.g.

# ```python
# assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
# assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
# assert has_close_elements([10, 10.1, 10.2], 0.15) == True
# assert has_close_elements([], 1.0) == False
# assert has_close_elements([1.5], 0.5) == False
# ```

import re
import subprocess
from typing import Tuple
from lats.cache import Cache


def run_command(cmd: str) -> str:
    # collect stdout and stderr (concat)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return (result.stdout.decode("utf-8") + result.stderr.decode("utf-8")).strip()

def run_command_with_exitcode(cmd: str) -> Tuple[str, int]:
    # collect stdout and stderr (concat)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    text = (result.stdout.decode("utf-8") + result.stderr.decode("utf-8")).strip()
    return text, result.returncode


def extract_python_code(text):
    # 3 cases
    # <straight source code> -> <straight source code>
    # ```<code>\n<code>``` -> <code>\n<code>
    # ```python\n<code>\n<code>\n``` -> <code>\n<code>
    if "```" in text:
        result = re.findall(r"```(.*?)```", text, re.DOTALL)[0]
    else:
        result = text
    
    if result.startswith("python\n"):
        result = result[7:]

    return result


def test():
    text = """
```python
assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([10, 10.1, 10.2], 0.15) == True
assert has_close_elements([], 1.0) == False
assert has_close_elements([1.5], 0.5) == False
```
    """
    print(extract_python_code(text))


def print_cache(name=None):
    cache = Cache(name)
    for k, v in cache.items():
        print(k)
        print("===")
        print(v)
        print("-" * 80)


if __name__ == "__main__":
    test()
