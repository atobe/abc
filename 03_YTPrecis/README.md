# Workflow summarizes many YT videos into one shorter video

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

6. **Set up YouTube API Keys**

- https://www.youtube.com/watch?v=uz7dY8qTFJw
- export YT_API_KEY=...

7. **Run the agent**

```bash
ytprecis precis "Apple's WWDC 2024 AI announcements"
open output.html
```

It might take multiple runs, some of the Pydantic structures are large and fail sometimes.
I've had to try 2-3 times sometimes.
The cache ensures you are not redoing any work that has already finished successfully.

8. **Examine/edit the cache**

```bash
ytprecis cache list
ytprecis cache delete edit.2c127f8f5e8da3600d4cc0c943a8e8bd
```

This will delete the final edit for instance.

| Item                                        | Label                                     |
|---------------------------------------------|-------------------------------------------|
| search_results.2c127f8f5e8da3600d4cc0c943a8e8bd | search_results                 |
| p2dhZ3AoDDt                                 | transcript for video p2dhZ3AoDDt                     |
| points.p2dhZ3AoDDt                          | extracted points for video                          |
| organized_points.2c127f8f5e8da3600d4cc0c943a8e8bd | organized_points               |
| edit.2c127f8f5e8da3600d4cc0c943a8e8bd       | video edit                            |
