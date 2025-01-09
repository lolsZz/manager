"""
Command line interface for the Dify installer.
"""
import click
import sys
import logging
from .setup import DifyInstaller
from .integration import create_installer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_step(msg):
    """Print a step message with formatting."""
    click.echo(click.style(f"⚡ {msg}", fg='blue'))

def print_success(msg):
    """Print a success message with formatting."""
    click.echo(click.style(f"✅ {msg}", fg='green'))

def print_error(msg):
    """Print an error message with formatting."""
    click.echo(click.style(f"❌ {msg}", fg='red'))

@click.group()
def cli():
    """Dify Installation CLI"""
    pass

@cli.command()
@click.option('--path', default=None, help='Installation path for Dify')
@click.option('--web/--no-web', default=False, help='Start web interface for installation')
def install(path, web):
    """Install Dify with interactive progress tracking."""
    if web:
        from .web import main as web_main
        web_main()
        return

    # Create installer integration
    dify_installer = create_installer(installation_path=path)
    def progress_callback(step, progress, message):
        if progress >= 0:
            print_step(f"{step}: {message}")
    dify_installer.set_progress_callback(progress_callback)
    try:
        dify_installer.run_installation()
        print_success("Dify installation completed successfully! 🎉")
        
        print_success("Dify installation completed successfully! 🎉")
        click.echo("\nYou can now:")
        click.echo("1. Start the backend server: cd ~/dify/api && flask run")
        click.echo("2. Start the frontend: cd ~/dify/web && npm start")
        
    except Exception as e:
        print_error(f"Installation failed: {str(e)}")
        sys.exit(1)

@cli.command()
def verify():
    """Verify Dify installation."""
    installer = DifyInstaller()
    try:
        if installer.verify_installation():
            print_success("Dify installation verification passed!")
        else:
            print_error("Dify installation verification failed!")
            sys.exit(1)
    except Exception as e:
        print_error(f"Verification error: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main()