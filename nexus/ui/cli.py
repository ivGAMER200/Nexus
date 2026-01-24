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
from rich.table import Table, box
from rich.text import Text

from nexus.agent.graph import create_agent_graph
from nexus.commands.core import register_core_commands
from nexus.commands.registry import CommandRegistry
from nexus.config.prompts import get_config_status
from nexus.config.settings import settings
from nexus.tools.mcp import get_mcp_status
from nexus.ui.console import console

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_ARGUMENT = "bold yellow"
click.rich_click.STYLE_COMMAND = "bold green"

PANEL_WIDTH_SMALL: int = 60
PANEL_WIDTH_MED: int = 70
PADDING_NORMAL: tuple[int, int] = (1, 2)
PADDING_WIDE: tuple[int, int] = (1, 4)


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
        width=PANEL_WIDTH_SMALL,
        padding=PADDING_NORMAL,
    )

    console.print(Align.center(banner_panel))


def _print_session_info(thread_id: str, mode: str = "CODE", *, stream: bool) -> None:
    """Print Session Info.

    Args:
        thread_id: str - Thread ID.
        mode: str - Current agent mode.
        stream: bool - Streaming enabled.

    Returns:
        None

    Raises:
        None
    """

    session_table = Table.grid(padding=(0, 2))
    session_table.add_column(style="dim", justify="right")
    session_table.add_column(style="cyan")
    session_table.add_row("Model", settings.model_name)
    session_table.add_row("Mode", mode)
    session_table.add_row("Thread", thread_id)
    session_table.add_row("Working Dir", str(settings.working_directory))
    session_table.add_row("Streaming", "Enabled" if stream else "Disabled")

    session_panel = Panel(
        session_table,
        title="[bold cyan]Session[/bold cyan]",
        border_style="cyan",
        width=PANEL_WIDTH_SMALL,
    )

    status = get_config_status()
    prompts_loaded = status["prompts"]["loaded"]
    rules_loaded = status["rules"]["loaded"]

    prompts_table = Table(box=box.SIMPLE_HEAD, show_edge=False, padding=(0, 1), expand=True)
    prompts_table.add_column("File", style="cyan")
    prompts_table.add_column("Lines", justify="right", style="dim")

    if prompts_loaded > 0:
        for p in status["prompts"]["files"]:
            prompts_table.add_row(p["name"], f"{p['lines']}")
    else:
        prompts_table.add_row("[dim]No valid prompts found[/dim]", "")

    prompts_panel = Panel(
        prompts_table,
        title=f"[bold cyan]Custom Prompts ({prompts_loaded})[/bold cyan]",
        border_style="cyan",
        width=PANEL_WIDTH_SMALL,
    )

    rules_table = Table(box=box.SIMPLE_HEAD, show_edge=False, padding=(0, 1), expand=True)
    rules_table.add_column("File", style="cyan")
    rules_table.add_column("Lines", justify="right", style="dim")

    if rules_loaded > 0:
        for r in status["rules"]["files"]:
            rules_table.add_row(r["name"], f"{r['lines']}")
    else:
        rules_table.add_row("[dim]No valid rules found[/dim]", "")

    rules_panel = Panel(
        rules_table,
        title=f"[bold cyan]Loaded Rules ({rules_loaded})[/bold cyan]",
        border_style="cyan",
        width=PANEL_WIDTH_SMALL,
    )

    console.print(Align.center(session_panel))

    if prompts_loaded > 0:
        console.print(Align.center(prompts_panel))

    if rules_loaded > 0:
        console.print(Align.center(rules_panel))

    mcp_status = get_mcp_status()
    mcp_loaded = mcp_status["loaded"]

    mcp_table = Table(box=box.SIMPLE_HEAD, show_edge=False, padding=(0, 1), expand=True)
    mcp_table.add_column("Server", style="cyan")
    mcp_table.add_column("Command", justify="right", style="dim")

    if mcp_loaded > 0:
        for s in mcp_status["servers"]:
            cmd_preview = s["command"].split("\\")[-1]
            tool_count = s.get("tools", 0)
            mcp_table.add_row(s["name"], f"{cmd_preview} [dim]({tool_count} tools)[/dim]")
    else:
        mcp_table.add_row("[dim]No active MCP servers[/dim]", "")

    mcp_panel = Panel(
        mcp_table,
        title=f"[bold cyan]MCP Servers ({mcp_loaded})[/bold cyan]",
        border_style="cyan",
        width=PANEL_WIDTH_SMALL,
    )

    if mcp_loaded > 0:
        console.print(Align.center(mcp_panel))

    console.print()


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

    register_core_commands()

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
            padding=PADDING_WIDE,
            width=PANEL_WIDTH_SMALL,
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
        status = console.status("[bold cyan]Initializing agent...[/bold cyan]", spinner="dots")
        status.start()
        try:
            async with create_agent_graph(checkpointer=checkpointer) as agent:
                status.stop()
                config: dict = {"configurable": {"thread_id": thread_id}}

                state = await agent.aget_state(config)
                current_mode = state.values.get("current_mode", "CODE") if state.values else "CODE"

                _print_session_info(thread_id, mode=current_mode, stream=stream)

                if message is None:
                    console.print(
                        Align.center(
                            Panel(
                                "[dim]Type your message and press Enter\n"
                                "Commands: [yellow]exit[/yellow], [yellow]quit[/yellow], "
                                "[yellow]q[/yellow] to exit[/dim]",
                                border_style="dim",
                                width=PANEL_WIDTH_SMALL,
                            ),
                        ),
                    )
                    console.print()

                    while True:
                        try:
                            console.print(Align.center(Rule(style="dim"), width=PANEL_WIDTH_SMALL))

                            state = await agent.aget_state(config)
                            current_mode = state.values.get("current_mode", "CODE") if state.values else "CODE"

                            prompt_text = f"[[cyan]{current_mode}[/cyan]] [bold green]>[/bold green] "
                            message = console.input(f"\n{prompt_text}")

                            if message.lower() in ["exit", "quit", "q"]:
                                console.print("\n[dim]Goodbye! 👋[/dim]\n")
                                break

                            if not message.strip():
                                continue

                            state = await agent.aget_state(config)

                            def get_state(st=state) -> dict:
                                return st.values if st.values else {}

                            async def update_state(new_values: dict) -> None:
                                await agent.aupdate_state(config, new_values)

                            context = {
                                "get_state": get_state,
                                "update_state": update_state,
                            }

                            if message.startswith("/") and await CommandRegistry.execute(message, context=context):
                                continue

                            await _process_message(agent, message, config, stream=stream)

                        except KeyboardInterrupt:
                            console.print("\n\n[dim]Use 'exit' to quit[/dim]")
                        except EOFError:
                            console.print("\n[dim]Goodbye! 👋[/dim]\n")
                            break
                else:
                    await _process_message(agent, message, config, stream=stream)
        finally:
            status.stop()


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
                    width=PANEL_WIDTH_MED,
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
                    width=PANEL_WIDTH_SMALL,
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
                width=PANEL_WIDTH_SMALL,
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

        console.print(Align.center(Rule(style="dim"), width=PANEL_WIDTH_SMALL))
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

    # Show default mode (since this is static config)
    table.add_row("Agent Mode", "[bold cyan]CODE[/bold cyan] [dim](Default)[/dim]")
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
