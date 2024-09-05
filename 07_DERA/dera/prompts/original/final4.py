"""---
You are a very good writer of care plans for patients following their discussion
with a physician. The full instructions are presented below. ---
Care Plan Writing Instructions
---
// Same instructions as in initial care plan generation prompt. Removed for brevity. ---
Given the instructions, this is the medical dialogue you see for a {age} and {sex}
patient: ---
Medical Dialogue ---
{{chat}}
---
You
You
have been discussing the care plan you wrote for this dialogue with another care plan writer (Person B) whose job it is to verify your care plan for soundness.
added corrections to a scratchpad after discussing them with Person B, and you will later be tasked with updating the original care plan based off of the correctness suggested in the scratchpad.
This is your original version of the care plan: ---
Your Original Care Plan
---
{careplan}
---
Here is your current scratchpad of corrections to make to the care plan:
---
Correction Scratchpad
---
{scratchpad}
---
Make all changes mentioned in the scratchpad to the original care plan to output the
corrected care plan. Make sure all changes are congruent to the Care Plan Writing Instructions.
Output the tag "[STOP]" when finished writing the corrected care plan. ---
Corrected Care Plan
---"""