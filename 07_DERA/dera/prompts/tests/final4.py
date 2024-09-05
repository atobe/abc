from .tpf import test_plan_format

prompt_template = f"""---
You are a very good writer of test cases for python functions. The full instructions are presented below. ---
Test Plan Writing Instructions
{test_plan_format}
---
This is the original function specification and signature:
{{function}}
You have been discussing the test plan you wrote for this dialogue with another test plan writer (Person B) whose job it is to verify your test plan for soundness.You added corrections to a scratchpad after discussing them with Person B, and you will later be tasked with updating the original test plan based off of the correctness suggested in the scratchpad.
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
Make all changes mentioned in the scratchpad to the original test plan to output the
corrected test plan. Make sure all changes are congruent to the Test Plan Writing Instructions. Just output the test plan comment and code. Do not write anything else.
Corrected Test Plan:
"""