from .tpf import test_plan_format

prompt_template = f"""---
You (Person A) are a very good writer of test cases for python functions. The full instructions are presented below. ---
{test_plan_format}
----
Test Plan Writing Instructions
{{function}}
---
You are discussing the test plan you wrote for this function with another test plan writer (Person B) whose job it is to verify your test plan for soundness. Person B will give you points for correction and it will be your job to add the points of correction to a scratchpad if you agree with them.
This is your original version of the test plan: ---
Your Original Test Plan
---
{{testplan}}
---
Here is your current scratchpad of corrections to make to the test plan:
---
Correction Scratchpad
---
{{scratchpad}}
---
You are generally very confident about the test plan you wrote, however, when presented with compelling arguments by the verifying test plan writer, you add to the correction scratchpad. You also suggest any edits of your own in case you notice a mistake.
This is the test plan discussion so far: ---
Test Plan Discussion
---
{{discussion}}
---
Respond with the following format:
ScratchpadUpdates:
<your_scratchpad_updates_here>

ResponseToPersonB:
<your_response_here>
---
Example Response 1:

ScratchpadUpdates:
Add the test case for fib(0) numbers to the TestBoundaryCases class.

ResponseToPersonB:
Thanks for your review. I've found some issues myself and look forward to your feedback.
---
Example Response 2:

ScratchpadUpdates:
Add the test case for fib(0) numbers to the TestBoundaryCases class.
Add negative numbers to the TestBoundaryCases class.

ResponseToPersonB:
I agree with your suggestion to add the test case for negative numbers to the TestBoundaryCases class. 
I will make the change in the test plan.
---
ok, start your response:
"""

if __name__ == '__main__':
    print(prompt_template)