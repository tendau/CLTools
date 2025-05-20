# CLLM - A simple CLI for Gemini LLM interactions

✨ A command-line interface for interacting with Google's Gemini LLM ✨

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd CLLM

# Install the package
pip install -e .
```

## Configuration

Create a `.env` file in your home directory with your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

```bash
# Ask Gemini a question
cllm ask "What is the capital of France?"

# Get help
cllm --help
```

## Commands

- `ask`: Ask a question to the Gemini LLM model
