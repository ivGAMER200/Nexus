"""Core Commands Module.

Implementation of core slash commands.
"""

from rich.align import Align
from rich.panel import Panel
from rich.table import Table, box
from rich.text import Text

from nexus.commands.registry import CommandRegistry
from nexus.config.settings import settings
from nexus.tools.mcp import _active_mcp_tools_info, get_mcp_status
from nexus.ui.console import console


class HelpCommand:
    """Help Command Class.

    Lists available slash commands.

    Inherits:
        None

    Attrs:
        name: str - Command name.
        description: str - Command description.

    Methods:
        execute(args): Execute help command.
    """

    name = "help"
    description = "Show available slash commands"

    def execute(self, args: list[str]) -> None:
        """Execute help command.

        Args:
            args: list[str] - Command arguments.

        Returns:
            None

        Raises:
            None
        """

        CommandRegistry.show_help()


class AboutCommand:
    """About Command Class.

    Shows application information.

    Inherits:
        None

    Attrs:
        name: str - Command name.
        description: str - Command description.

    Methods:
        execute(args): Execute about command.
    """

    name = "about"
    description = "Show application information"

    def execute(self, args: list[str]) -> None:
        """Execute about command.

        Args:
            args: list[str] - Command arguments.

        Returns:
            None

        Raises:
            None
        """

        banner_text = Text.assemble(
            ("NEXUS", "bold white"),
            (" - AI Coding Agent\n", "bold cyan"),
            ("Powered by LangChain, LangGraph & MCP", "dim cyan"),
        )

        panel = Panel(
            Align.left(banner_text),
            border_style="cyan",
            width=60,
            padding=(1, 2),
        )
        console.print(panel)
        console.print()


class ConfigCommand:
    """Config Command Class.

    Shows current configuration settings.

    Inherits:
        None

    Attrs:
        name: str - Command name.
        description: str - Command description.

    Methods:
        execute(args): Execute config command.
    """

    name = "config"
    description = "Show current configuration"

    def execute(self, args: list[str]) -> None:
        """Execute config command.

        Args:
            args: list[str] - Command arguments.

        Returns:
            None

        Raises:
            None
        """

        table = Table(
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

        console.print(table)
        console.print()


class MCPsCommand:
    """MCPs Command Class.

    Shows detailed info about active MCP servers and tools.

    Inherits:
        None

    Attrs:
        name: str - Command name.
        description: str - Command description.

    Methods:
        execute(args): Execute mcps command.
    """

    name = "mcps"
    description = "Show active MCP servers and tool details"

    def execute(self, args: list[str]) -> None:
        """Execute mcps command.

        Args:
            args: list[str] - Command arguments.

        Returns:
            None

        Raises:
            None
        """

        status = get_mcp_status()
        mcp_loaded = status["loaded"]

        mcp_panel_title = f"[bold cyan]Active MCP Servers ({mcp_loaded})[/bold cyan]"

        if mcp_loaded == 0:
            console.print(
                Panel(
                    "[dim]No active MCP servers found.[/dim]",
                    title=mcp_panel_title,
                    border_style="cyan",
                    width=60,
                ),
            )
            return

        for server in status["servers"]:
            name = server["name"]
            command = server["command"]
            tool_count = server["tools"]

            server_table = Table(box=box.SIMPLE, show_edge=False, padding=(0, 1), expand=True)
            server_table.add_column("Property", style="dim", width=15)
            server_table.add_column("Value", style="white")

            server_table.add_row("Command", command)
            server_table.add_row("Tool Count", str(tool_count))

            tools_info = _active_mcp_tools_info.get(name, [])
            if tools_info:
                server_table.add_row("", "")
                server_table.add_row("[cyan]Tools[/cyan]", "")
                for t in tools_info:
                    server_table.add_row("", f"[bold]{t['name']}[/bold]: {t['description']}")

            console.print(
                Panel(
                    server_table,
                    title=f"[bold green]{name}[/bold green]",
                    border_style="dim",
                    expand=False,
                ),
            )
            console.print()


def register_core_commands() -> None:
    """Register core commands.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    CommandRegistry.register(HelpCommand())
    CommandRegistry.register(AboutCommand())
    CommandRegistry.register(ConfigCommand())
    CommandRegistry.register(MCPsCommand())
