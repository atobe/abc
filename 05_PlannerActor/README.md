# Implementation of Planner + Actor

[Slide Deck](https://docs.google.com/presentation/d/1-2iSAl5Qnwkmmi44IYwvH5gL1kke99MpJpZjPEA7AHE/edit?usp=sharing)

## Running the code

1. **Clone this repo**

```bash
   git clone <repo_url>
```

2. **Set up a virtual environment**

```bash
python -m venv pa_venv
source pa_venv/bin/activate
```

3. **Install the package**

```bash
cd abc/05_PlannerActor
pip install -r requirements.txt
cd raal
pip install -e .
cd ../planner_actor
pip install -e .
```

4. **Set up OpenAI or other LLM provider API keys**

- https://platform.openai.com/docs/quickstart

5. **Choose a model and export MODEL env var**

I used gpt-4-0125-preview. GPT-4 proper is better but this is cheaper.

```bash
export MODEL=gpt-4-0125-preview
```

6. **(Optional) Run RAAL to get the idea of ReAct**

```bash
raal
```

7. **Run Planner+Actor**

```bash
planner_actor "What is Einstein's age to the power of 2?"
planner_actor "What is the age difference between Albert Einstein and Issac Newton?"
```
