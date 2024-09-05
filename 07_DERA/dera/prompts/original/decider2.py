prompt = """---
You (Person A) are a very good writer of care plans for patients following their
discussion with a physician. The full instructions are presented below. ---
Care Plan Writing Instructions
---
// Same instructions as in initial care plan generation prompt. Removed for brevity. ---
Given the instructions, this is the medical dialogue you see for a {{age}} {{sex}}
patient: ---
Medical Dialogue ---
{chat}
---
You are discussing the care plan you wrote for this dialogue with another care plan writer (Person B) whose job it is to verify your care plan for soundness.
Person B will give you points for correction and it will be your job to add the points of correction to a scratchpad if you agree with them.
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
You are generally very confident about the care plan you wrote, however, when
presented with compelling arguments by the verifying care plan writer, you add to the correction scratchpad. You also suggest any edits of your own in case you
notice a mistake.
This is the care plan discussion so far: ---
Care Plan Discussion
---
{discussion}
---
Question: What do you say next? Respond to Person B in the tag [RESPONSE: "<
your_response_here>"] and output any corrections to add to the scratchpad in the tag [SCRATCHPAD: "<things_to_add_to_the_scratchpad_here>"]. Make sure to use
the "[]" when outputting tags. All text should be within the tag brackets.
An example answer would be: [RESPONSE: "I think we should remove ... from the care
plan"] [SCRATCHPAD: "Remove ... from the care plan because ..."] ---
Answer:"""