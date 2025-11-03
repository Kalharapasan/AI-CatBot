# AI-CatBot

A lightweight AI chatbot project. This repository contains the core chatbot code and knowledge used by the bot.

## Overview

AI-CatBot is a small chatbot project that demonstrates a simple conversational assistant powered by local code and data files. It is intended as a starting point for experimentation and extension.

## Features

- Simple command-line entry point (`main.py`).
- Local knowledge stored in `ai_knowledge.json`.
- Small and easy to extend for experiments and learning.

## Requirements

- Python 3.8 or newer

## Quick start

1. Ensure Python is installed and available on your PATH.
1. From the repository root, run the bot with:

```powershell
python main.py
```

1. Follow any prompts printed by `main.py`.

## Setup & development

These steps help you create an isolated environment and run the project locally.

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv
```

1. Activate the virtual environment (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

1. Run the bot:

```powershell
python main.py
```

Notes:

- There is no `requirements.txt` in this repository by default. Add one if your project needs external packages.
- For Windows Command Prompt use `\.venv\Scripts\activate.bat` instead of the PowerShell command above.

## Example conversation

Here is a simple example showing how the bot might interact on the command line. Exact prompts depend on `main.py`'s implementation.

User: Hello

Bot: Hi — I'm AI-CatBot. How can I help you today?

User: Tell me something about yourself.

Bot: I'm a small experimental chatbot that uses a local knowledge file (`ai_knowledge.json`) to answer simple questions.

User: What's the weather like?

Bot: I don't have live weather data. I can answer questions that are in my local knowledge base or help with general information.

## `ai_knowledge.json` schema and example

`ai_knowledge.json` stores local knowledge used by the bot. A minimal example entry could look like this:

```json
[
  {
    "id": "greeting",
    "trigger": ["hello", "hi", "hey"],
    "response": "Hello! I'm AI-CatBot — ask me anything about this project.",
    "metadata": { "lang": "en", "source": "builtin" }
  }
]
```

Recommended fields:

- `id` — unique string identifier for the entry.
- `trigger` — array of phrases or keywords that match user input.
- `response` — text the bot should return when the trigger matches.
- `metadata` — optional object for language, tags, or provenance.

To add knowledge, edit `ai_knowledge.json` and add new entries following the example. How entries are matched and used depends on the code in `main.py`.

## Project structure

- `main.py` — program entry point.
- `ai_knowledge.json` — local knowledge store used by the bot.
- `README` — legacy/untouched file (kept for backward compatibility).

## Contributing

Feel free to open issues or pull requests. Small, well-scoped changes (bug fixes, documentation, examples) are easiest to review.

## License

This project does not include an explicit license file. If you plan to reuse or distribute code, consider adding a `LICENSE` file describing permissions and restrictions.

---

If you want the original `README` file removed or replaced, tell me and I can update it as well.
