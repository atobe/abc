from pathlib import Path
from typing import List, Tuple
from devtools import pprint
from .complete import complete
from .extractor import extract_sections, extract_code

responses_fp = None


def print_block(title, text):
    print(f"=== {title} ".ljust(80, "="))
    print(text)
    print("=" * 80)


def get_cached_response(response_fp: Path) -> str:
    if response_fp.exists():
        return response_fp.read_text()
    return None


def step(system_prompt: str, prompt: str, step_num: int):
    response_fp = responses_fp / f"response-{step_num}.txt"
    prompt_fp = responses_fp / f"prompt-{step_num}.txt"
    prompt_fp.write_text(prompt)
    had_result = result = get_cached_response(response_fp)
    if result:
        return result
    result = complete(system_prompt=system_prompt, user_prompt=prompt)
    if not had_result:
        response_fp.write_text(result)
    return result


TestPlan = str
ScratchpadUpdateAndDiscussion = Tuple[str, str]
ScratchpadUpdateDiscussionDone = Tuple[str, str, bool]


def initial_step(function: str) -> TestPlan:
    from .prompts.tests.gen1 import prompt_template

    prompt = prompt_template.format(function=function)
    test_plan = step("You are part of a test team", prompt, 1)
    return test_plan


def decider_step(function, test_plan, scratchpad, discussion, step_num) -> ScratchpadUpdateAndDiscussion:
    from .prompts.tests.decider2 import prompt_template

    prompt = prompt_template.format(
        function=function,
        testplan=test_plan,
        scratchpad=scratchpad,
        discussion=discussion,
    )
    result = step("You are part of a test team", prompt, step_num)
    sections = extract_sections(result)
    scratchpad = sections.get("ScratchpadUpdates")
    print_block("ScratchpadUpdates", scratchpad)
    discussion = discussion + "\n\n" + sections.get("ResponseToPersonB")
    return scratchpad, discussion


def check_done(response: str) -> bool:
    return "DONE" in response


def researcher_step(
    function, test_plan, scratchpad, discussion, step_num
) -> ScratchpadUpdateDiscussionDone:
    from .prompts.tests.researcher3 import prompt_template

    prompt = prompt_template.format(
        function=function,
        testplan=test_plan,
        scratchpad=scratchpad,
        discussion=discussion,
    )
    result = step("You are part of a test team", prompt, step_num)
    sections = extract_sections(result)
    scratchpad = sections.get("CorrectionScratchpad", scratchpad)
    print_block("CorrectionScratchpad", scratchpad) 
    discussion = discussion + "\n\n" + sections.get("ResponseToPersonA")
    done = check_done(result)
    return scratchpad, discussion, done


def final_step(function, test_plan, scratchpad, step_num):
    """Use the last scratchpad and initial testplan to generate the revised testplan and tests"""

    from .prompts.tests.final4 import prompt_template

    prompt = prompt_template.format(
        function=function,
        testplan=test_plan,
        scratchpad=scratchpad,
    )
    result = step("You are part of a test team", prompt, step_num)
    code = extract_code(result)[0]
    return code


def run_dera(tag: str, function: str) -> str:
    global responses_fp

    responses_fp = Path(__file__).parents[1] / "responses" / tag
    responses_fp.mkdir(parents=True, exist_ok=True)

    print("Running DERA")
    print("generating initial test plan - step 1")
    step = 1
    test_plan = initial_step(function)
    initial_test_plan_fp = responses_fp / "initial_test_plan.py"
    code = extract_code(test_plan)[0]
    initial_test_plan_fp.write_text(code)
    scratchpad = ""
    discussion = ""
    for n in range(3):
        step += 1
        print(f"decider step {step}")
        scratchpad, discussion = decider_step(function, test_plan, scratchpad, discussion, step)
        step += 1
        print(f"researcher step {step}")
        scratchpad, discussion, done = researcher_step(
            function, test_plan, scratchpad, discussion, step
        )
        if done:
            print("conversation done")
            break
    step += 1
    print(f"final step {step}")
    code = final_step(function, test_plan, scratchpad, step)

    code_fp = responses_fp / "final_test_plan.py"
    code_fp.write_text(code)

    return code
