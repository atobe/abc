# This is an implementation of an agent that follows a single news story over a long period

[Slide Deck](https://docs.google.com/presentation/d/13th5xg_bCaHaHcXkL_lI9UcOpWclmeBOySF29je2DSE/edit?usp=sharing)

## Running the code

1. **Clone this repo**

```bash
   git clone <repo_url>
```

2. **Set up a virtual environment**

```bash
python -m venv news_venv
source news_venv/bin/activate
```

3. **Install the package**

```bash
cd 02_News
pip install -e .
```

4. **Set up OpenAI or other LLM provider API keys**

- https://platform.openai.com/docs/quickstart

5. **Run the agent**

```bash
agent_news reset
agent_news update # run this multiple times
```

Look in news/cache/knowledge.txt to see updates
