"""CLI Module.

Rich-Click CLI for Nexus.
"""

import asyncio
from typing import Any

import rich_click as click
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from rich.align import Align
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from nexus.agent.graph import create_agent_graph
from nexus.config.settings import settings
from nexus.ui.console import console

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_ARGUMENT = "bold yellow"
click.rich_click.STYLE_COMMAND = "bold green"


def print_banner() -> None:
    """Print Nexus Banner.

    Display a modern, responsive banner for Nexus.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    banner_text = Text.assemble(
        ("NEXUS", "bold white"),
        (" - AI Coding Agent\n", "bold cyan"),
        ("Powered by LangChain & LangGraph", "dim cyan"),
    )

    banner_panel = Panel(
        Align.center(banner_text),
        border_style="cyan",
        width=60,
        padding=(1, 2),
    )

    console.print(Align.center(banner_panel))


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0", prog_name="Nexus")
def cli(ctx: click.Context) -> None:
    """Nexus CLI.

    🤖 **Nexus - AI Coding Agent**

    A modern, production-ready AI coding assistant powered by LangChain and LangGraph.

    **Main Features:**
    - 🔄 Stateful conversations with checkpointing
    - 🛠️ Powerful file and shell tools
    - 👤 Human-in-the-loop approvals
    - 📊 Full observability with LangSmith
    - 🎨 Beautiful terminal UI
    """

    if ctx.invoked_subcommand is None:
        print_banner()
        welcome_panel = Panel(
            "[bold white]Welcome to Nexus![/bold white]\n\n"
            "[dim]Available commands:[/dim]\n"
            "  [cyan]nexus chat[/cyan]     - Start interactive chat\n"
            "  [cyan]nexus history[/cyan]  - View conversation history\n"
            "  [cyan]nexus config[/cyan]   - Show configuration\n\n"
            "[dim]For help:[/dim] [yellow]nexus --help[/yellow]",
            border_style="cyan",
            padding=(1, 4),
            width=60,
        )
        console.print(Align.center(welcome_panel))


@cli.command()
@click.argument("message", required=False)
@click.option(
    "--thread-id",
    "-t",
    help="Thread ID for conversation continuity",
    default="default",
)
@click.option(
    "--stream/--no-stream",
    default=True,
    help="Stream responses in real-time",
)
def chat(message: str | None, thread_id: str, *, stream: bool) -> None:
    """Chat Command.

    💬 Start an interactive chat session with the agent.

    **Examples:**
    ```bash
    $ nexus chat "List all Python files"
    $ nexus chat --thread-id my-project
    $ nexus chat --no-stream "Refactor main.py"
    ```
    """

    asyncio.run(_chat(message, thread_id, stream=stream))


async def _chat(message: str | None, thread_id: str, *, stream: bool) -> None:
    """Internal Chat Function.

    Internal async chat function.
    """

    print_banner()

    async with AsyncSqliteSaver.from_conn_string(settings.checkpoint_db) as checkpointer:
        with console.status("[bold cyan]Initializing agent...[/bold cyan]", spinner="dots"):
            agent: Any = await create_agent_graph(checkpointer=checkpointer)

        config: dict = {"configurable": {"thread_id": thread_id}}

        info_table = Table.grid(padding=(0, 2))
        info_table.add_column(style="dim", justify="right")
        info_table.add_column(style="cyan")
        info_table.add_row("Model", settings.model_name)
        info_table.add_row("Thread", thread_id)
        info_table.add_row("Working Dir", str(settings.working_directory))
        info_table.add_row("Streaming", "Enabled" if stream else "Disabled")

        info_panel = Align.center(
            Panel(
                info_table,
                title="[bold cyan]Session Info[/bold cyan]",
                border_style="cyan",
                padding=(1, 2),
                width=60,
            ),
        )
        console.print(info_panel)
        console.print()

        if message is None:
            console.print(
                Align.center(
                    Panel(
                        "[dim]Type your message and press Enter\n"
                        "Commands: [yellow]exit[/yellow], [yellow]quit[/yellow], [yellow]q[/yellow] to exit[/dim]",
                        border_style="dim",
                        width=60,
                    ),
                ),
            )
            console.print()

            while True:
                try:
                    console.print(Align.center(Rule(style="dim"), width=60))
                    message = console.input("\n[bold green]>[/bold green] ")

                    if message.lower() in ["exit", "quit", "q"]:
                        console.print("\n[dim]Goodbye! 👋[/dim]\n")
                        break

                    if not message.strip():
                        continue

                    await _process_message(agent, message, config, stream=stream)

                except KeyboardInterrupt:
                    console.print("\n\n[dim]Use 'exit' to quit[/dim]")
                except EOFError:
                    console.print("\n[dim]Goodbye! 👋[/dim]\n")
                    break
        else:
            await _process_message(agent, message, config, stream=stream)


async def _process_message(agent: Any, message: str, config: dict, *, stream: bool) -> None:
    """Process Message.

    Process a single message.

    Args:
        agent: any - Agent instance.
        message: str - Message to process.
        config: dict - Configuration.
        stream: bool - Stream responses.

    Returns:
        None

    Raises:
        None
    """

    input_state: dict = {
        "messages": [HumanMessage(content=message)],
        "iteration_count": 0,
        "working_directory": str(settings.working_directory),
        "tool_calls_made": [],
        "files_modified": [],
    }

    console.print()

    if stream:
        console.print("[bold cyan]Assistant[/bold cyan]")
        console.print()

        async for event in agent.astream_events(input_state, config, version="v2"):
            kind: str = event["event"]

            if kind == "on_chat_model_stream":
                content: str = event["data"]["chunk"].content
                if content:
                    console.print(content, end="")

            elif kind == "on_tool_start":
                tool_name: str = event["name"]
                console.print(f"\n\n[dim]┌─ Tool: [cyan]{tool_name}[/cyan][/dim]")

            elif kind == "on_tool_end":
                console.print("[dim]└─ ✓ Completed[/dim]")

        console.print("\n")

    else:
        with console.status("[bold cyan]Processing...[/bold cyan]", spinner="dots"):
            result: dict = await agent.ainvoke(input_state, config)

        last_message: Any = result["messages"][-1]
        console.print(
            Align.center(
                Panel(
                    Markdown(last_message.content),
                    title="[bold cyan]Assistant[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2),
                    width=70,
                ),
            ),
        )
        console.print()


@cli.command()
@click.option(
    "--thread-id",
    "-t",
    help="Thread ID to show history for",
    default="default",
)
@click.option(
    "--limit",
    "-n",
    help="Number of checkpoints to show",
    default=10,
    type=int,
)
def history(thread_id: str, limit: int) -> None:
    """History Command.

    📜 Show conversation history for a specific thread.
    """

    asyncio.run(_show_history(thread_id, limit))


async def _show_history(thread_id: str, limit: int) -> None:
    """Show History.

    Show conversation history.
    """

    print_banner()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Loading history...", total=None)

        async with AsyncSqliteSaver.from_conn_string(settings.checkpoint_db) as checkpointer:
            config: dict = {"configurable": {"thread_id": thread_id}}

            checkpoints: list = [checkpoint async for checkpoint in checkpointer.alist(config)]  # ty:ignore[invalid-argument-type]

    if not checkpoints:
        console.print(
            Align.center(
                Panel(
                    f"[yellow]No history found for thread '[cyan]{thread_id}[/cyan]'[/yellow]",
                    border_style="yellow",
                    width=60,
                ),
            ),
        )
        return

    console.print(
        Align.center(
            Panel(
                f"[bold]Conversation History[/bold]\n"
                f"[dim]Thread:[/dim] [cyan]{thread_id}[/cyan]\n"
                f"[dim]Total Checkpoints:[/dim] [cyan]{len(checkpoints)}[/cyan]",
                border_style="cyan",
                width=60,
            ),
        ),
    )
    console.print()

    for i, checkpoint in enumerate(reversed(checkpoints[:limit]), 1):
        state: dict = checkpoint.checkpoint["channel_values"]
        messages: list = state.get("messages", [])

        console.print(f"[bold cyan]Checkpoint {i}[/bold cyan]")
        console.print()

        for msg in messages:
            role: str = msg.__class__.__name__
            content: str = getattr(msg, "content", "")

            if role == "HumanMessage":
                console.print(f"[bold green]User:[/bold green] {content}")
            elif role == "AIMessage":
                console.print(f"[bold cyan]Assistant:[/bold cyan] {content[:200]}...")
            else:
                console.print(f"[dim]{role}:[/dim] {content[:100]}...")

        console.print(Align.center(Rule(style="dim"), width=60))
        console.print()


@cli.command()
def config() -> None:
    """Config Command.

    ⚙️ Show current application configuration and environment settings.
    """

    print_banner()

    table: Table = Table(
        title="[bold cyan]Configuration[/bold cyan]",
        show_header=True,
        header_style="bold white",
        border_style="cyan",
        padding=(0, 1),
    )
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Model", f"[green]{settings.model_name}[/green]")
    table.add_row("Temperature", f"[yellow]{settings.temperature}[/yellow]")
    table.add_row("Max Tokens", f"[yellow]{settings.max_tokens}[/yellow]")
    table.add_row("Max Iterations", f"[yellow]{settings.max_iterations}[/yellow]")
    table.add_row(
        "Approval Required",
        "[green]Yes[/green]" if settings.approval_required else "[red]No[/red]",
    )
    table.add_row("Working Directory", f"[dim]{settings.working_directory}[/dim]")
    table.add_row(
        "LangSmith Tracing",
        "[green]Enabled[/green]" if settings.langsmith_tracing else "[red]Disabled[/red]",
    )
    table.add_row("Checkpoint DB", f"[dim]{settings.checkpoint_db}[/dim]")
    table.add_row("Log Level", f"[yellow]{settings.log_level}[/yellow]")

    console.print(Align.center(table))
    console.print()


if __name__ == "__main__":
    cli()


__all__: list[str] = ["cli"]
