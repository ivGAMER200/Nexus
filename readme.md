# Nexus - AI Coding Agent

**Nexus is a modern, CLI-based AI coding agent that transforms natural language into efficient, production-ready code.**

Powered by **LangChain**, **LangGraph**, and **LangSmith**, Nexus provides a persistent, stateful coding assistant with advanced capabilities like human-in-the-loop approvals, full observability, and the **Model Context Protocol (MCP)** for extensible tooling.

## ✨ Features

- 🔄 **Stateful Conversations** - Persistent conversation history with SQLite checkpointing.
- 🔌 **Model Context Protocol (MCP)** - Connect external tools using the open standard MCP.
- 🛠️ **Powerful Built-in Tools** - File operations, shell commands, and code analysis.
- 👤 **Human-in-the-Loop** - Secure approval workflows for tool execution.
- 📊 **Full Observability** - Complete tracing and debugging with LangSmith.
- 🎨 **Beautiful CLI** - Rich terminal interface with real-time streaming and status panels.
- 🚀 **Production-Ready** - Built with modern best practices, type safety, and structured logging.

## 🏗️ Architecture

Nexus is built on a robust stack:

- **LangChain** - Orchestration and tool integration.
- **LangGraph** - State machine for reliable agent workflows.
- **LangSmith** - Observability, tracing, and evaluation.
- **MCP (Model Context Protocol)** - Standardized connection to external data and tools.
- **Rich-Click** - Modern, beautiful CLI interface.
- **Pydantic** - Strict configuration and validation.
- **SQLite** - Local persistence for conversation threads.

## 📋 Prerequisites

- Python 3.10+
- OpenAI API key
- (Optional) LangSmith API key for tracing
- (Optional) Docker/Node.js for specific MCP servers

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
   source .venv/Scripts/activate  # Windows (Git Bash)
   
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

4. **Configure environment:**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your keys:
   ```env
   OPENAI_API_KEY=sk-...
   LANGSMITH_API_KEY=ls__...  # Optional
   LANGSMITH_PROJECT=nexus
   LANGSMITH_TRACING=true
   ```

## 🔌 Model Context Protocol (MCP)

Nexus supports the Model Context Protocol, allowing you to easily extend its capabilities with external servers.

### Configuration

Create or edit `.nexus/mcp_config.json` in your project root to define servers.

**Example Configuration:**

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Projects"]
    }
  }
}
```

Nexus automatically loads these servers, counts their tools, and injects their descriptions into the agent's system prompt so it knows exactly how to use them.

## 💻 Usage

### Interactive Chat

Start the agent in interactive mode:

```bash
nexus chat
```

You will see a dashboard showing the active session, loaded prompts, rules, and connected MCP servers.

### Command Line Mode

Send a single instruction without entering interactive mode:

```bash
nexus chat "Refactor main.py to use async/await"
```

### Thread Management

Maintain context across sessions using thread IDs:

```bash
nexus chat --thread-id feature-auth "Add login endpoint"
nexus chat --thread-id feature-auth "Now add logout"
```

### View History

Review past conversations:

```bash
nexus history --thread-id feature-auth
```

### Configuration Check

Verify your settings and loaded components:

```bash
nexus config
```

## 🏗️ Project Structure

```
nexus/
├── nexus/
│   ├── agent/          # Core agent logic
│   │   ├── graph.py    # LangGraph definition & tool loading
│   │   ├── nodes.py    # Agent reasoning nodes
│   │   └── state.py    # State schema
│   │
│   ├── tools/          # Tool definitions
│   │   ├── mcp.py      # MCP client & configuration handler
│   │   ├── file_ops.py # Built-in file tools
│   │   └── shell.py    # Built-in shell tools
│   │
│   ├── config/         # Configuration
│   │   ├── settings.py # Pydantic settings
│   │   └── prompts.py  # System prompts
│   │
│   ├── ui/             # Terminal Interface
│   │   ├── cli.py      # CLI entry point & UI components
│   │   └── console.py  # Rich console instance
│   │
│   └── main.py         # App entry point
│
├── .nexus/             # Local config directory
│   ├── mcp_config.json # MCP server definitions
│   └── prompts/        # Custom user prompts
│
└── readme.md           # Documentation
```

## ⚙️ Configuration Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_BASE_URL` | OpenAI base URL | None |
| `LANGSMITH_TRACING` | Enable tracing | true |
| `LOG_LEVEL` | Logging verbosity | INFO |
| `CHECKPOINT_DB` | SQLite DB path | checkpoints.db |

## 🤝 Contributing

Contributions are welcome! Please follow the code style guidelines:

1.  Use **Ruff** for linting.
2.  Use **MyPy/Ty** for type checking.
3.  Ensure all functions have docstrings.

```bash
ruff check .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain & LangGraph** for the agent framework.
- **Anthropic & MCP Team** for the Model Context Protocol standard.
- **Rich** for the terminal UI.

---

**Made with ❤️ by Rohit Vilas Ingole**
