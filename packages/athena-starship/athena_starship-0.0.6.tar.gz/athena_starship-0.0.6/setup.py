# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['athena_starship', 'athena_starship.tools']

package_data = \
{'': ['*']}

install_requires = \
['swarms==4.9.3', 'transformers']

setup_kwargs = {
    'name': 'athena-starship',
    'version': '0.0.6',
    'description': 'Paper - Pytorch',
    'long_description': '# Athena\n\n## Install\n`$ pip install athena-starship`\n\n## Usage\n```bash\npython3 sam_altman.py\n```\n\n```python\nimport os\n\nfrom dotenv import load_dotenv\n\n# Import the OpenAIChat model and the Agent struct\nfrom swarms import Agent\nfrom athena_starship.llama import llama\nfrom athena_starship.memory import ChromaDB\nfrom athena_starship.tools.google_calendar import calendar\n\n# Load the environment variables\nload_dotenv()\n\n# Get the API key from the environment\napi_key = os.environ.get("OPENAI_API_KEY")\n\n# Initilaize the chromadb client\nchromadb = ChromaDB(\n    metric="cosine",\n    verbose=True,\n    n_results=3,\n)\n\n## Initialize the workflow\nagent = Agent(\n    llm=llama,\n    agent_name="Sam Altman",\n    agent_description="Sam Altman Agent, CEO of OpenAI.",\n    system_prompt="You\'re Sam Altman, CEO of OpenAI.",\n    max_loops="auto",\n    interactive=True,\n    autosave=True,\n    dashboard=True,\n    long_term_memory=chromadb,\n    stopping_token="<DONE>",\n    verbose=True,\n    # tools=[calendar],\n)\n\n# Run the workflow on a task\nagent.run(\n    "What are the 3 traits you look for before investing in a seed"\n    " stage startup?"\n)\n\n```\n\n# License\nMIT\n\n\n# Todo\n- [ ] Make csv of few shot prompt examples for various tool usages\n- [ ] Make tools for airtable, google calendar, notion, gmail\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Starship-Ventures/Athena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
