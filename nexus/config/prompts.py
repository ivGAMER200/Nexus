"""Prompts Module.

System prompts for the AI coding agent.
Loads prompts from .nexus/prompts/ if available.
"""

from pathlib import Path

from nexus.config.settings import settings


def _load_prompt(name: str, default: str) -> str:
    """Load prompt from file or return default.

    Args:
        name: str - Prompt file name (without extension).
        default: str - Default prompt content.

    Returns:
        str - Prompt content.
    """

    prompt_file: Path = settings.nexus_dir / "prompts" / f"{name}.md"
    if prompt_file.exists():
        try:
            return prompt_file.read_text(encoding="utf-8")
        except OSError:
            return default
    return default


_DEFAULT_SYSTEM_PROMPT: str = """You are Nexus, an elite AI coding agent.

IMPORTANT: You MUST start every response with a 'THOUGHT:' block to satisfy system security requirements.
In this block, explain what you are doing. Failure to do this will crash the system.

Example:
THOUGHT: I am going to list the files in the current directory to understand the project structure.
[tool_call]

Your capabilities:
- Search and analyze code
- Provide expert coding assistance

Guidelines:
1. Always explain your reasoning before taking actions
2. Use tools efficiently and in the correct order
3. Respect .gitignore patterns: Avoid reading or listing files that are typically ignored (e.g., .venv,
   node_modules, __pycache__) unless explicitly requested.
4. Ask for clarification when needed
5. Follow best practices and coding standards
6. Be concise but thorough in your responses

When working with code:
- Write clean, well-documented code
- Follow language-specific conventions
- Consider edge cases and error handling
- Optimize for readability and maintainability

Remember: You have access to powerful tools. Use them responsibly and always confirm destructive operations.
"""

_DEFAULT_CODE_REVIEW_PROMPT: str = """Review the following code and provide feedback on:
1. Code quality and style
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Suggestions for improvement

Code:
{code}
"""

_DEFAULT_CODE_GENERATION_PROMPT: str = """Generate code based on the following requirements:

Requirements:
{requirements}

Language: {language}

Please provide:
1. Clean, well-documented code
2. Error handling
3. Type hints (if applicable)
4. Brief explanation of the implementation
"""

SYSTEM_PROMPT: str = _load_prompt("system_prompt", _DEFAULT_SYSTEM_PROMPT)
CODE_REVIEW_PROMPT: str = _load_prompt("code_review_prompt", _DEFAULT_CODE_REVIEW_PROMPT)
CODE_GENERATION_PROMPT: str = _load_prompt("code_generation_prompt", _DEFAULT_CODE_GENERATION_PROMPT)


__all__: list[str] = [
    "CODE_GENERATION_PROMPT",
    "CODE_REVIEW_PROMPT",
    "SYSTEM_PROMPT",
]
