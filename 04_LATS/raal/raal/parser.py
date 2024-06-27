import re
from typing import List, Union
import ast

from .model import Thought, Action, Answer, FunctionCall

examples = [
    "Thought: I need to find out the capital of France.\n\nAction: search('capital of France')\nThe capital of France is Paris.\nENDHEREDOC",
    "Thought: The capital of France is a well-known fact.\n\nAnswer: The capital of France is Paris.",
    "Thought: I need to search for the capital of France.\n\nAction: search('capital of France')\n\nObservation: The capital of France is Paris.",
    "Thought: I need to read the file spec.txt and implement the specification therein.\n\nAction: read_file('spec.txt', with_line_numbers=True)\n\nObservation"
]


class UnknownSectionType(Exception):
    pass


class SectionParseError(Exception):
    pass


class FuncExtractVisitor:
    def extract_details(self, node):
        return self.visit(node)

    def visit(self, node):
        return getattr(self, f"visit_{node.__class__.__name__}")(node)

    # Module
    def visit_Module(self, node):
        return self.visit(node.body[0])

    # Expr
    def visit_Expr(self, node):
        return self.visit(node.value)

    # Call
    def visit_Call(self, node):
        func_name = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        kwargs = {self.visit(kw.arg): self.visit(kw.value) for kw in node.keywords}
        return func_name, args, kwargs

    # Name
    def visit_Name(self, node):
        return node.id

    # Constant
    def visit_Constant(self, node):
        return node.value

    # Str
    def visit_Str(self, node):
        return node.s

    def visit_str(self, node):
        return node

    # Num
    def visit_Num(self, node):
        return node.n

    # Attribute
    def visit_Attribute(self, node):
        return f"{self.visit(node.value)}.{node.attr}"


class Parser:
    def parse(self, text: str):
        text = text.strip()
        # split over "Thought:", "Action:", "Observation:"
        parts = re.split(r"(Thought|Action|Observation|Answer):", text)
        parts = list(filter(lambda s: s != "", parts))

        sections = []
        for i in range(0, len(parts), 2):
            section = ":".join(parts[i : i + 2])
            sections.append(section)

        return self.parse_sections(sections)

    def parse_sections(self, sections: List[str]):
        # return list(filter(None, [self.parse_section(section) for section in sections]))
        # either we see a Final Answer or (Thought, Action) in that order
        # stop when we have seen either of these
        seen_thought = False
        seen_action = False
        parses = []
        for section in sections:
            parsed = self.parse_section(section)
            if isinstance(parsed, Answer):
                parses.append(parsed)
                return parses
            if isinstance(parsed, Thought):
                seen_thought = True
                parses.append(parsed)
            if isinstance(parsed, Action):
                seen_action = True
                parses.append(parsed)
            if seen_thought and seen_action:
                return parses
        return parses

    def parse_section(self, section: str):
        # extract the first word
        first_word = section.split(":", 1)[0]
        if first_word not in ["Thought", "Action", "Observation", "Answer"]:
            raise UnknownSectionType(f"Unknown section type: {first_word}")
        return getattr(self, f'parse_{first_word.lower().replace(" ", "_")}')(section)

    def parse_thought(self, section: str):
        return Thought(text=section.split(":", 1)[1].strip(), original_text=section)

    def parse_answer(self, section: str):
        return Answer(text=section.split(":", 1)[1].strip(), original_text=section)

    def parse_action(self, lines: Union[str, List[str]]):
        # if isinstance(lines, list):
        #     text = '\n'.join(lines)
        # else:
        #     text = lines

        # text = text.replace('\\\\', '').replace('\\', '')

        if isinstance(lines, str):
            lines = lines.strip()
            lines = lines.split("\n")
        # the rest of the action line looks like a python function call, parse as such
        # example - Action: eat_cookies(3, type="choc chip")
        action_line = lines.pop(0)

        # check for contamination
        parsed_lines = [action_line]
        code = action_line.split(":", 1)[1].strip()
        try:
            node = ast.parse(code)
            func_name, args, kwargs = FuncExtractVisitor().extract_details(node)
        except:
            raise SectionParseError(f"Error parsing action: {action_line}")
        heredoc = None
        if len(lines) > 0:
            # heredoc is all the remaining lines unless you find one like Observation: ...
            heredoc_lines = []
            while len(lines) > 0:
                line = lines.pop(0)
                if (
                    line.startswith("Observation:")
                    or line.startswith("Action:")
                    or line.startswith("ENDHEREDOC")
                ):
                    lines.insert(0, line)
                    break
                heredoc_lines.append(line)
                parsed_lines.append(line)
            heredoc = "\n".join(heredoc_lines)
            # heredoc should end with single newline
            # trim then add
            heredoc = heredoc.rstrip() + "\n"
        return Action(
            function_call=FunctionCall(
                function_name=func_name, args=args, kwargs=kwargs, heredoc=heredoc
            ),
            original_text="\n".join(parsed_lines),
        )

    def parse_observation(self, section: str):
        # return None to indicate drop
        return None


def main():
    for example in examples:
        # print(example)
        print(Parser().parse(example))
        print()


if __name__ == "__main__":
    main()
