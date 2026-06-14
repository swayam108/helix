"""CLI interface for HELIX"""

import asyncio
import sys
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

from helix.core.commander import Commander
from helix.utils.logger import setup_logger

console = Console()
setup_logger()


@click.group()
def cli():
    """HELIX: Local-First Multi-Agent AI Operating System"""
    pass


@cli.command()
@click.argument('request', nargs=-1, required=True)
def execute(request):
    """Execute a task request"""
    user_request = " ".join(request)
    
    console.print(Panel(
        f"[bold cyan]HELIX[/bold cyan] - Executing: {user_request}",
        style="bold green"
    ))
    
    try:
        commander = Commander()
        result = asyncio.run(commander.execute(user_request))
        
        # Display results
        console.print(f"\n[bold]Status:[/bold] {result.status}")
        console.print(f"[bold]Execution Time:[/bold] {result.execution_time:.2f}s")
        
        if result.tasks:
            console.print(f"\n[bold]Tasks Executed:[/bold] {len(result.tasks)}")
            for task in result.tasks:
                console.print(f"  - {task.id}: {task.description}")
        
        if result.output:
            console.print(f"\n[bold]Output:[/bold]\n{result.output}")
        
        if result.errors:
            console.print(f"\n[red]Errors:[/red]")
            for error in result.errors:
                console.print(f"  - {error}")
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
def status():
    """Show system status"""
    commander = Commander()
    status_info = commander.get_system_status()
    
    table = Table(title="HELIX System Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in status_info.items():
        if isinstance(value, float):
            table.add_row(key, f"{value:.1f}%" if key.endswith("_percent") else f"{value:.2f}")
        else:
            table.add_row(key, str(value))
    
    console.print(table)


@cli.command()
@click.option('--limit', default=10, help='Number of recent results to show')
def history(limit):
    """Show execution history"""
    commander = Commander()
    results = commander.get_execution_history(limit)
    
    if not results:
        console.print("[yellow]No execution history found[/yellow]")
        return
    
    table = Table(title="Execution History")
    table.add_column("Status", style="cyan")
    table.add_column("Time (s)", style="green")
    table.add_column("Tasks", style="magenta")
    table.add_column("Errors", style="red")
    
    for result in results:
        table.add_row(
            result.status,
            f"{result.execution_time:.2f}",
            str(len(result.tasks)),
            str(len(result.errors))
        )
    
    console.print(table)


@cli.command()
def interactive():
    """Start interactive HELIX session"""
    console.print(Panel(
        "[bold cyan]Welcome to HELIX[/bold cyan]\n"
        "Type 'help' for commands, 'exit' to quit",
        style="bold green"
    ))
    
    commander = Commander()
    
    while True:
        try:
            user_input = input("\n[HELIX] > ").strip()
            
            if not user_input:
                continue
            if user_input.lower() == "exit":
                console.print("[yellow]Goodbye![/yellow]")
                break
            if user_input.lower() == "status":
                status_info = commander.get_system_status()
                console.print(f"[cyan]System Status:[/cyan]")
                for k, v in status_info.items():
                    console.print(f"  {k}: {v}")
                continue
            
            result = asyncio.run(commander.execute(user_input))
            console.print(f"\n[green]✓ Completed[/green] ({result.execution_time:.2f}s)")
            if result.output:
                console.print(f"[cyan]{result.output}[/cyan]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
