from rich.console import Console
from toml import load

import os
import subprocess

from ascender.settings import IS_UNIX


class RunnerLogic:
    console: Console

    def __init__(self, console: Console, command: str | None = None) -> None:
        self.command = "" if not command else command
        self.toml_path = f"{os.getcwd()}/pyproject.toml"
        self.console = console
    
    def is_project(self):
        """
        Check if the current directory is an AscenderFramework project or not.
        """
        directory = os.getcwd()

        if os.path.exists(f"{directory}/start.py") and os.path.exists(f"{directory}/core") and os.path.exists(f"{directory}/pyproject.toml"):
            toml_data = load(self.toml_path)
            if toml_data["tool"]["poetry"]["name"] != "ascender-framework":
                return False
            
            return True

    def invoke(self):
        if not self.is_project():
            self.console.print("[red]Error:[/red] [bold]Cannot recognize project directory[/bold]")
            self.console.print("[bold yellow]Make sure you are in the root of any AscenderFramework project.[/bold yellow]")
            return
        
        directory = os.getcwd()
        
        if IS_UNIX:
            subprocess.run(f"source {directory}/.asc_venv/bin/activate && python3 start.py {self.command}", shell=True, executable='/bin/bash')
            return
        
        subprocess.run(f". {directory}/.asc_venv/bin/activate && python start.py {self.command}", shell=True)
    
    def invoke_clean(self, hide_output: bool = False):
        if not self.is_project():
            self.console.print("[red]Error:[/red] [bold]Cannot recognize project directory[/bold]")
            self.console.print("[bold yellow]Make sure you are in the root of any AscenderFramework project.[/bold yellow]")
            return
        
        directory = os.getcwd()
        
        if IS_UNIX:
            _process = subprocess.run(f"source {directory}/.asc_venv/bin/activate && {self.command}", 
                           stdout=subprocess.DEVNULL if hide_output else None, 
                           stderr=subprocess.DEVNULL if hide_output else None, shell=True, executable='/bin/bash')
            return _process
        
        _process = subprocess.run(f". {directory}/.asc_venv/bin/activate && {self.command}",
                        stdout=subprocess.DEVNULL if hide_output else None, 
                        stderr=subprocess.DEVNULL if hide_output else None, shell=True)
        
        return _process
    