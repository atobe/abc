from human_eval.data import read_problems


problems = None


def _get_case(case_number):
    global problems
    if not problems:
        problems = read_problems()
    case_name = f"HumanEval/{case_number}"
    return problems[case_name]
