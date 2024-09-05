from devtools import pprint
from typing import List

import re

def extract_code(text) -> List[str]:
    # Define a regex pattern to match the code sections
    # may start with ```python or just ```
    # and end with ```
    pattern = r"```(?:python)?\n(?P<code>.+?)\n```"

    # Find all matches using the regex pattern
    matches = re.finditer(pattern, text, re.DOTALL)

    # Extract the code sections from the matches
    code_sections = [match.group("code") for match in matches]

    return code_sections

def trim_section(text):
    lines = text.strip().splitlines()
    # remove any leading or trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop(-1)
    # remove any leading or trailing lines '---'
    while lines and lines[0].strip() == '---':
        lines.pop(0)
    while lines and lines[-1].strip() == '---':
        lines.pop(-1)
    return '\n'.join(lines)

def extract_sections(text):
    # Define a regex pattern to match the sections and their contents
    pattern = r"(?P<section>\w+):\n(?P<content>.+?)(?=\n\w+:|\Z)"
    
    # Find all matches using the regex pattern
    matches = re.finditer(pattern, text, re.DOTALL)
    
    # Create a dictionary to store the results
    sections = {match.group("section"): trim_section(match.group("content")) for match in matches}
    
    return sections

def main():
    from pathlib import Path
    fp = Path(__file__).parents[2] / 'responses' / 'response-2.txt'
    text = fp.read_text()

    # Extract sections as a dictionary
    result = extract_sections(text)

    # Print the result
    pprint(result)

if __name__ == "__main__":
    main()
