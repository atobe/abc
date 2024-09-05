test_plan_format = """
Start by writing an outline (as a python comment) describing the TestCases classes and test cases (methods) you will write.
Follow this by the actual test cases themeselves enclosed in triple backticks.

# TestPlanOutline:
# class TestBoundaryCases(unittest.TestCase):
# - test 0
#
# class TestGeneralCases(unittest.TestCase):
# - test 1
# - test 2
#
# class TestErrorCases(unittest.TestCase):
# - test negative
# - test large negative

```
import unittest
from fut import fibonacci

class TestBoundaryCases(unittest.TestCase):
    def test_0(self):
        self.assertEqual(fibonacci(0), 0)


class TestGeneralCases(unittest.TestCase):
    def test_1(self):
        self.assertEqual(fibonacci(1), 1)

    def test_2(self):
        self.assertEqual(fibonacci(2), 1)


class TestErrorCases(unittest.TestCase):
    def test_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_large_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-30)
            
if __name__ == '__main__':
    unittest.main()
```
"""