# Nexus - AI Coding Agent

**Nexus is a CLI-based AI coding agent that transforms natural language into efficient, production-ready code!**

Powered by LangChain, LangGraph, and LangSmith, Nexus provides a modern, production-ready AI coding assistant with advanced features like stateful conversations, human-in-the-loop approvals, and full observability.

## ✨ Features

- 🔄 **Stateful Conversations** - Persistent conversation history with checkpointing
- 🛠️ **Powerful Tools** - File operations, shell commands, and more
- 👤 **Human-in-the-Loop** - Approval workflows for sensitive operations
- 📊 **Full Observability** - Complete tracing with LangSmith
- 🎨 **Beautiful UI** - Rich terminal interface with streaming responses
- 🔌 **Extensible** - Easy to add new tools and capabilities
- 🚀 **Production-Ready** - Built with modern best practices

## 🏗️ Architecture

Nexus is built using:

- **LangChain** - LLM orchestration and tool integration
- **LangGraph** - State machine for agent workflows
- **LangSmith** - Observability and tracing
- **Rich-Click** - Beautiful CLI interface
- **Pydantic** - Type-safe configuration
- **SQLite** - Persistent checkpointing

## 📋 Prerequisites

- Python 3.14.2 or higher
- OpenAI API key
- Optional: LangSmith API key for tracing

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/datarohit/nexus.git
cd nexus
```

2. **Create and activate virtual environment:**

```bash
# Using uv (recommended)
uv venv
source .venv/Scripts/activate  # Git Bash on Windows

# Or using standard venv
python -m venv .venv
source .venv/Scripts/activate
```

3. **Install dependencies:**

```bash
# Using uv (fastest)
uv pip install -e .

# Or using pip
pip install -e .
```

4. **Configure environment variables:**

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=ls__...  # Optional
LANGSMITH_PROJECT=nexus
LANGSMITH_TRACING=true
```

## 💻 Usage

### Interactive Chat

Start an interactive chat session:

```bash
nexus chat
```

### Single Message

Send a single message:

```bash
nexus chat "List all Python files in the current directory"
```

### Thread Management

Continue a previous conversation:

```bash
nexus chat --thread-id my-project "What did we discuss earlier?"
```

### View History

View conversation history for a thread:

```bash
nexus history --thread-id my-project
```

### Configuration

View current configuration:

```bash
nexus config
```

### Streaming

Enable or disable streaming responses:

```bash
# With streaming (default)
nexus chat "Generate a Python function"

# Without streaming
nexus chat --no-stream "Generate a Python function"
```

## 🎯 Examples

### File Operations

```bash
nexus chat "Read the contents of main.py"
nexus chat "Create a new file called test.py with a hello world function"
nexus chat "List all files in the src directory"
```

### Code Generation

```bash
nexus chat "Generate a Python function to calculate fibonacci numbers"
nexus chat "Create a REST API endpoint using FastAPI"
nexus chat "Write unit tests for the calculator module"
```

### Code Review

```bash
nexus chat "Review the code in utils.py and suggest improvements"
nexus chat "Check for security issues in the authentication module"
```

### Shell Commands

```bash
nexus chat "Run the tests using pytest"
nexus chat "Check the git status"
```

## 🏗️ Project Structure

```
nexus/
├── nexus/
│   ├── agent/          # LangGraph state machine
│   │   ├── graph.py    # Agent graph definition
│   │   ├── nodes.py    # Graph nodes
│   │   └── state.py    # State definitions
│   │
│   ├── tools/          # LangChain tools
│   │   ├── file_ops.py # File operations
│   │   └── shell.py    # Shell commands
│   │
│   ├── memory/         # Memory management
│   │   └── conversation.py
│   │
│   ├── config/         # Configuration
│   │   ├── settings.py # Pydantic settings
│   │   └── prompts.py  # System prompts
│   │
│   ├── ui/             # User interface
│   │   ├── cli.py      # Rich-Click CLI
│   │   └── console.py  # Rich console
│   │
│   ├── utils/          # Utilities
│   │   ├── logging.py  # Structured logging
│   │   └── tracing.py  # LangSmith tracing
│   │
│   └── main.py         # Entry point
│
├── docs/               # Documentation
├── .env.example        # Environment template
├── pyproject.toml      # Project configuration
└── readme.md           # This file
```

## ⚙️ Configuration

Configuration is managed through environment variables and can be customized in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_BASE_URL` | OpenAI base URL | None |
| `LANGSMITH_API_KEY` | LangSmith API key | None |
| `LANGSMITH_PROJECT` | LangSmith project name | nexus |
| `LANGSMITH_TRACING` | Enable LangSmith tracing | true |
| `LOG_LEVEL` | Logging level | INFO |
| `DEBUG` | Debug mode | false |

## 💾 Memory Management

Nexus uses **LangGraph's state-based memory** for conversation management:

- **Persistent Checkpointing** - All conversations are automatically saved to SQLite
- **Thread-based Sessions** - Use `--thread-id` to continue previous conversations
- **Message History** - Full conversation context maintained across sessions
- **No Manual Memory** - LangGraph handles message persistence automatically

The `memory/` module provides a simple `ConversationMemory` class for basic use cases, but the agent primarily uses LangGraph's built-in state management (`AgentState`) which integrates seamlessly with checkpointing.

## 🔧 Development

### Code Style

The project follows strict code style guidelines:

- **Ruff** for linting
- **isort** for import sorting
- **Type hints** for all functions
- **Docstrings** following Google style

### Running Linters

```bash
# Run ruff
ruff check .

# Run isort
isort .
```

## 📊 Observability

Nexus integrates with LangSmith for full observability:

1. **Tracing** - Every LLM call is traced
2. **Debugging** - Inspect prompts and responses
3. **Analytics** - Cost and latency tracking
4. **Evaluation** - Test and improve performance

View traces at: https://smith.langchain.com

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](license) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Powered by [LangGraph](https://langchain-ai.github.io/langgraph/)
- Observability by [LangSmith](https://smith.langchain.com)
- UI by [Rich](https://rich.readthedocs.io/) and [Rich-Click](https://github.com/ewels/rich-click)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by Rohit Vilas Ingole**
