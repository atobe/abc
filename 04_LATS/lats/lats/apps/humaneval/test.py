from typing import Tuple

from lats.apps.humaneval.lib import _get_case
from lats.utils import extract_python_code, run_command, run_command_with_exitcode
from lats.cache import Cache
from lats.llm import call_llm

suffix = """
def run_tests():
    passing_tests = 0
    total_tests = len(test_lines)
    
    for test in test_lines:
        try:
            exec(test)
            passing_tests += 1
        except AssertionError:
            pass
            print(f'Test failed: {test}')
    
    print(f"{passing_tests} / {total_tests}")

# Run the tests
run_tests()
"""

given_suffix = """
check({function_name})
"""

make_a_test_prompt1 = """
You are an expert python programmer. You are given a function intended to test students. We are making an automated test rig. We need a set of tests (up to 5) that the function should pass. They should take the form of assert statements, one per line. The function is as follows:
{function}

Just reply with the test statements, nothing else."""

make_a_test_prompt2 = """
You are an expert python programmer. You are given a function intended to test students. We have some existing tests that the function should pass. We need you to write additional tests (up to 5) that the function should pass. They should take the form of assert statements, one per line. The function is as follows:
{function}

{existing_tests}

Just reply with the test statements, nothing else."""


def value(case_number, source) -> Tuple[float, str]:
    test_filepath = make_test(
        source,
        case_number,
        use_canonical_test=True,
    )
    result, code = run_command_with_exitcode(f"python {test_filepath}")
    print('-'*80)
    print(result)
    print('-'*80)

    if code != 0:
        return 0.0, result

    try:
        passing, total = result.strip().split("/")
        return float(passing) / float(total), result
    except:
        return 0, result

def run_test(test_file):
    result = run_command(f"python {test_file}")
    if result.strip() == "":
        result = "All tests passed"
    return result




def extract_test_cases_from_canonical_test_file(test_source):
    lines = test_source.split("\n")
    test_lines = [line.lstrip() for line in lines if "assert" in line]
    return "\n".join(test_lines)


def make_canonical_test_file(source, case_number) -> str:
    case = _get_case(case_number)
    source = extract_python_code(source)

    test_source = extract_test_cases_from_canonical_test_file(case["test"])
    test_source = test_source.replace("candidate", case["entry_point"])

    test_source = (
        "test_lines = [\n"
        + ",\n".join([f'    "{line}"' for line in test_source.split("\n")])
        + "\n]"
    )

    content = source + "\n\n" + test_source + "\n" + suffix

    with open("/tmp/test.py", "w") as f:
        f.write(content)

    # format with black
    run_command(f"black /tmp/test.py")

    return "/tmp/test.py"


def make_invented_test_file(source, case_number):
    case = _get_case(case_number)
    source = extract_python_code(source)
    test_source = TestMaker()._make_a_test(case_number)
    test_source = test_source.replace("candidate", case["entry_point"])

    test_source = (
        "test_lines = [\n"
        + ",\n".join([f'"{line}"' for line in test_source.split("\n")])
        + "\n]"
    )

    content = source + "\n" + test_source + "\n" + suffix

    with open("/tmp/test.py", "w") as f:
        f.write(content)

    # format with black
    run_command(f"black /tmp/test.py")

    return "/tmp/test.py"


def make_test(source, case_number, use_canonical_test=False):
    return (
        make_canonical_test_file(source, case_number)
        if use_canonical_test
        else make_invented_test_file(source, case_number)
    )


def check_test_cases(case_number):
    case = _get_case(case_number)
    canonical_solution = case["prompt"] + case["canonical_solution"]
    test_source = TestMaker()._make_a_test(case_number)
    test_source = (
        "test_lines = [\n"
        + ",\n".join([f'"{line}"' for line in test_source.split("\n")])
        + "\n]"
    )
    content = canonical_solution + "\n" + test_source + "\n" + suffix

    with open("/tmp/test.py", "w") as f:
        f.write(content)

    # format with black
    run_command(f"black /tmp/test.py")

    return "/tmp/test.py"


class TestMaker:
    def __init__(self):
        self.test_cache = Cache("humaneval")

    def _make_a_test(self, case_number):
        if case_number in self.test_cache:
            result = self.test_cache[case_number]
            return result

        # get the canonical solution
        case = self.hev._get_case(case_number)
        # pprint(case)
        # print()

        function = case["prompt"] + "\n" + case["canonical_solution"]
        existing_tests = case["test"]
        # prompt = case['prompt']
        # ask LLM for test cases only
        # run the tests
        # prune any failing tests
        # cache the test cases
        messages = [
            {
                "role": "user",
                "content": make_a_test_prompt2.format(
                    function=function, existing_tests=existing_tests
                ),
            }
        ]
        result = call_llm(messages, check_cache=False)
        print("make a test llm result -----------------------")
        print(result)
        print("-" * 80)
        result = extract_python_code(result)

        self.test_cache[case_number] = result
        return result


if __name__ == "__main__":
    source = """
from typing import List
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False"""
    # make_canonical_test_file(source, 0)
    # import os
    # os.system("cat /tmp/test.py")

    print(value(0, source))