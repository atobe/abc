humaneval0 = """
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    ''' Check if in given list of numbers, are any two numbers closer to each other than the given threshold.'''
"""

humaneval1 = """
def separate_paren_groups(paren_string: str) -> List[str]:
    ''' Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    '''
"""

humaneval2 = """
def truncate_number(number: float) -> float:
    ''' Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).'''
"""

from .dera import run_dera


def main():
    run_dera("humaneval0", humaneval0)
    # run_dera("humaneval1", humaneval1)
    # run_dera("humaneval1_dsc", humaneval1)
    # run_dera("humaneval2_gpt4", humaneval2)


if __name__ == "__main__":
    main()
