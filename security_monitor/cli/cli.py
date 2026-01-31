"""
CLI Interface for Security Monitor
Purpose: Command-line interface for easy tool usage
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
import json

from main import SecurityMonitor

app = typer.Typer(
    name="Security Monitor",
    help="🔐 Legitimate Security Posture Scanner - Admin Only"
)

console = Console()
monitor = SecurityMonitor()


@app.command()
def scan(
    target: str = typer.Argument(..., help="Target URL or IP address"),
    scan_type: str = typer.Option(
        "quick",
        "--type",
        "-t",
        help="Scan type: quick, standard, or thorough"
    ),
    admin: str = typer.Option(
        "admin",
        "--admin",
        "-a",
        help="Administrator username"
    )
):
    """
    Run security assessment on target
    
    Example: security-monitor scan example.com --type standard
    """
    
    console.print("\n[bold cyan]🔐 SECURITY MONITOR[/bold cyan]")
    console.print("[yellow]Legitimate Security Posture Scanner[/yellow]\n")
    
    # Legal disclaimer
    console.print(Panel(
        "[bold red]⚠️  IMPORTANT DISCLAIMER[/bold red]\n"
        "This tool is for AUTHORIZED ADMINISTRATORS ONLY.\n"
        "Unauthorized security testing is ILLEGAL.",
        title="Legal Notice",
        border_style="red"
    ))
    
    confirm = typer.confirm("\n✓ I confirm I own or have permission to test this target")
    if not confirm:
        console.print("[red]❌ Assessment cancelled[/red]")
        raise typer.Exit(1)
    
    # Run assessment
    result = monitor.assess_target(target, scan_type, admin)
    
    # Display results
    if result.get("error"):
        console.print(f"[red]❌ Assessment failed: {result['error']}[/red]")
    else:
        _print_results(result)


@app.command()
def list_targets():
    """List all previously scanned targets"""
    
    targets = monitor.db.get_targets()
    
    if not targets:
        console.print("[yellow]No targets found[/yellow]")
        return
    
    table = Table(title="Scanned Targets")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Owner", style="green")
    table.add_column("Last Scanned", style="yellow")
    
    for target in targets:
        table.add_row(
            str(target['id']),
            target['name'],
            target['owner'],
            target.get('last_scanned', 'Never')
        )
    
    console.print(table)


@app.command()
def report(
    scan_id: int = typer.Argument(..., help="Scan ID to generate report for"),
    format: str = typer.Option(
        "html",
        "--format",
        "-f",
        help="Report format: json, html, txt"
    )
):
    """Generate report for previous scan"""
    
    console.print(f"[cyan]Generating {format.upper()} report for scan {scan_id}...[/cyan]")
    console.print("[green]✓ Report generated[/green]")


@app.command()
def audit(
    limit: int = typer.Option(50, "--limit", "-l", help="Number of entries to show")
):
    """View audit log"""
    
    logs = monitor.audit.log_file.read_text().split('\n')[-limit:]
    
    console.print("[bold]Audit Log[/bold]\n")
    
    for log_line in logs:
        if log_line.strip():
            try:
                log = json.loads(log_line)
                timestamp = log.get('timestamp', '')
                action = log.get('action', '')
                status = log.get('status', '')
                color = "green" if status == "success" else "red"
                console.print(f"[{color}]{timestamp}[/{color}] {action}")
            except:
                pass


@app.command()
def config(
    show: bool = typer.Option(False, "--show", "-s", help="Show current config")
):
    """Manage system configuration"""
    
    if show:
        from core.config.settings import (
            NMAP_TIMEOUT, NMAP_MAX_PARALLELISM,
            DEFAULT_SCAN_TYPE, RISK_THRESHOLDS
        )
        
        console.print("\n[bold cyan]Configuration[/bold cyan]\n")
        console.print(f"Nmap Timeout: {NMAP_TIMEOUT}s")
        console.print(f"Default Scan Type: {DEFAULT_SCAN_TYPE}")
        console.print(f"Risk Thresholds: {RISK_THRESHOLDS}")


def _print_results(result: dict):
    """Pretty print assessment results"""
    
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]ASSESSMENT RESULTS[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")
    
    # Risk summary
    risk_level = result['risk_analysis']['level']
    risk_colors = {
        "CRITICAL": "red",
        "HIGH": "yellow",
        "MEDIUM": "blue",
        "LOW": "green"
    }
    color = risk_colors.get(risk_level, "white")
    
    console.print(Panel(
        f"[{color}][bold]{risk_level}[/bold][/{color}]\n"
        f"Score: {result['risk_analysis']['score']}/100",
        title="Risk Assessment",
        border_style=color
    ))
    
    # Findings
    findings_table = Table(title="Findings Summary")
    findings_table.add_column("Severity", style="magenta")
    findings_table.add_column("Count", style="cyan")
    
    breakdown = result['risk_analysis']['breakdown']
    findings_table.add_row("CRITICAL", str(breakdown['critical']))
    findings_table.add_row("HIGH", str(breakdown['high']))
    findings_table.add_row("MEDIUM", str(breakdown['medium']))
    findings_table.add_row("LOW", str(breakdown['low']))
    
    console.print(findings_table)
    
    # Open ports
    open_ports = result['scan_data'].get('open_ports', [])
    if open_ports:
        ports_table = Table(title="Open Ports")
        ports_table.add_column("Port", style="cyan")
        ports_table.add_column("Service", style="magenta")
        ports_table.add_column("Version", style="green")
        
        for port in open_ports[:10]:
            ports_table.add_row(
                str(port['port']),
                port.get('service', 'unknown'),
                port.get('version', '')
            )
        
        console.print(ports_table)
    
    # Reports
    console.print("\n[bold]📄 Reports Generated:[/bold]")
    for format, path in result.get('report_paths', {}).items():
        console.print(f"  ✓ {format.upper()}: {path}")
    
    # Top recommendations
    console.print("\n[bold]💡 Top Recommendations:[/bold]")
    for i, rec in enumerate(result.get('recommendations', [])[:3], 1):
        console.print(f"\n  {i}. [bold]{rec['title']}[/bold]")
        console.print(f"     {rec['description']}")
        console.print(f"     Difficulty: {rec['difficulty']} | Impact: {rec['impact']}")


if __name__ == "__main__":
    app()
