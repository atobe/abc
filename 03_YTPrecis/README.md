# This is an implementation of a workflow that can create a short summary video from many YT videos.

## Running the code

1. **Clone this repo**

```bash
   git clone <repo_url>
```

2. **Set up a virtual environment**

```bash
python -m venv ytprecis_venv
source ytprecis_venv/bin/activate
```

3. **Install the package**

```bash
cd abc/03_YTPrecis
pip install -r requirements.txt
pip install -e .
```

4. **Set up OpenAI or other LLM provider API keys**

- https://platform.openai.com/docs/quickstart

5. **Choose a model and export MODEL env var**

I used gpt-4-0125-preview. GPT-4 proper is better but this is cheaper.

```bash
export MODEL=gpt-4-0125-preview
```

5. **Set up YouTube API Keys**

- https://www.youtube.com/watch?v=uz7dY8qTFJw
- export YT_API_KEY=...

5. **Run the agent**

```bash
ytprecis precis "Apple WWDC 2024"
```

It might take multiple runs, some of the Pydantic structures are large and fail sometimes.
I've had to try 2-3 times sometimes.
The cache ensures you are not redoing any work that has already finished successfully.

