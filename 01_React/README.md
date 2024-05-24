# This is an implementation of the ReAct pattern

## Running the code

1. **Clone this repo**
```bash
   git clone <repo_url>
```
2. **Set up a virtual environment**
```bash
python -m venv react_venv
source react_venv/bin/activate
```

3. **Install the prerequisites**
```bash
cd 01_React
pip install -r requirements.txt
```

4. **Set up OpenAI or other LLM provider API keys**
- https://platform.openai.com/docs/quickstart

5. **Run the agent**
```bash
cd react
python __main__.py
```

## Resources

Paper [link](https://arxiv.org/abs/2210.03629)

Blog [link](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

GitHub [link](https://react-lm.github.io/)

Simon Willison's exposition [link](https://til.simonwillison.net/llms/python-react-pattern)

