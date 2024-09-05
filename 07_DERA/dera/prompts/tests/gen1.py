from .tpf import test_plan_format

prompt_template = f"""----
Comprehensive Unit Test Cases
----
You are a member of a test team tasked with writing a set of comprehensive unit test cases for a new function.
{test_plan_format}
----
Test Plan Writing Instructions
----
Now that you've seen an example, you will now write a test plan and unit tests of the same format (Outline, followed by python code).
The function you will write tests for is:
---- Function ----
{{function}}
---- Test Plan ----
# TestPlanOutline:
"""