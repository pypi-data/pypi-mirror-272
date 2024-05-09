# Athena

## Install
`$ pip install athena-starship`

## Usage
```bash
python3 sam_altman.py
```

```python
import os

from dotenv import load_dotenv

# Import the OpenAIChat model and the Agent struct
from swarms import Agent
from athena_starship.llama import llama
from athena_starship.memory import ChromaDB
from athena_starship.tools.google_calendar import calendar

# Load the environment variables
load_dotenv()

# Get the API key from the environment
api_key = os.environ.get("OPENAI_API_KEY")

# Initilaize the chromadb client
chromadb = ChromaDB(
    metric="cosine",
    verbose=True,
    n_results=3,
)

## Initialize the workflow
agent = Agent(
    llm=llama,
    agent_name="Sam Altman",
    agent_description="Sam Altman Agent, CEO of OpenAI.",
    system_prompt="You're Sam Altman, CEO of OpenAI.",
    max_loops="auto",
    interactive=True,
    autosave=True,
    dashboard=True,
    long_term_memory=chromadb,
    stopping_token="<DONE>",
    verbose=True,
    tools=[calendar],
)

# Run the workflow on a task
agent.run(
    "What are the 3 traits you look for before investing in a seed"
    " stage startup?"
)

```

# License
MIT


# Todo
- [ ] Make csv of few shot prompt examples for various tool usages
- [ ] Make tools for airtable, google calendar, notion, gmail
