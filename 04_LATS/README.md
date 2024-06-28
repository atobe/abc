# Implementation of LATS

[Slide Deck](https://docs.google.com/presentation/d/1gedRSTZB-f_glHojrwre7YwstcT0HdcRjnmzNE-1acI/edit?usp=sharing)

## Running the code

1. **Clone this repo**

```bash
   git clone <repo_url>
```

2. **Set up a virtual environment**

```bash
python -m venv lats_venv
source lats_venv/bin/activate
```

3. **Install the package**

```bash
cd abc/04_LATS
pip install -r requirements.txt
cd raal
pip install -e .
cd ../lats
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

7. **Run LATS on a HumanEval task**

```bash
lats run humaneval 0
```

7. **Run LATS on a general ReAct task**

```bash
lats run agent "What is the age difference between Albert Einstein and Issac Newton?"
```

