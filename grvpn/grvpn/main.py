from datetime import datetime, timezone
import os
import signal
import subprocess
import sys
import time
import threading
import webbrowser
import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from grvpn.openvpn import OpenVPN
from grvpn.vpn import VPN
from grvpn.auth import Sentinel, SENTINEL_AUTH_URL
from grvpn.sudo_manager import SudoManager

app = typer.Typer()
console = Console()

@app.command()
def login():
    """Login with Sentinel."""
    server_thread = threading.Thread(target=Sentinel.run_auth_server, daemon=True)
    server_thread.start()
    webbrowser.open(SENTINEL_AUTH_URL, new=1)
    
    with console.status("Waiting for Sentinel login...", spinner="dots"):
        server_thread.join()

    credentials = Sentinel.get_saved_credentials()
    if credentials:
        user_info = Sentinel.get_user_info()
        if user_info:
            with Live(render_login(user_info), refresh_per_second=1, console=console) as live:
                pass
        else:
            typer.echo("Failed to get user info. Please try again.")
    else:
        typer.echo("Login failed. Please try again.")

@app.command()
def connect():
    """Connect to the Gaucho Racing VPN."""
    if not Sentinel.verify_credentials():
        typer.echo("Credentials missing or expired. Please run `grvpn login`.")
        raise typer.Exit(code=1)

    profile = VPN.get_profile()
    valid = False

    if profile:
        profile_name = profile.split("/")[-1].split(".")[0]
        typer.echo(f"Profile found: {profile_name}")
        client = VPN.get_client_info(profile_name)
        if client:
            expires_at = datetime.fromisoformat(client["expires_at"].replace("Z", "+00:00"))
            if expires_at > datetime.now(timezone.utc):
                typer.echo("Profile is valid.")
                valid = True
            else:
                typer.echo("Profile is expired.")
    
    if not valid:
        with console.status("Generating new client...", spinner="dots"):
            client = VPN.new_client()
            if not client:
                typer.echo("Failed to generate profile.")
                raise typer.Exit(code=1)
        
        typer.echo(f"Generated new client: {client['id']}")
        VPN.save_profile(client["id"], client["profile_text"])
        profile = VPN.get_profile()

    typer.echo("")
    
    if not OpenVPN.check_cli():
        console.print("OpenVPN is not installed. Please install it first.", style="bold red")
        console.print("For macOS, use Homebrew: `brew install openvpn`.", style="dim")
        console.print("For Linux, use your distribution's package manager.", style="dim")
        console.print("For Windows, use the OpenVPN Connect client.", style="dim")
        raise typer.Exit(code=1)

    if not SudoManager.ensure_sudo_access():
        typer.echo("Failed to authenticate sudo access.")
        raise typer.Exit(code=1)

    OpenVPN.flush_routes()
    with console.status("Connecting to the Gaucho Racing VPN...", spinner="dots"):
        proc = OpenVPN.connect(profile)
        if proc:
            time.sleep(0.5)

    if not proc:
        typer.echo("Failed to connect.")
        raise typer.Exit(code=1)

    OpenVPN.set_dns()

    connected_time = time.time()
    ip = "0.0.0.0"
    ip = VPN.test_connection()['ip']
    expires_at = datetime.fromisoformat(client["expires_at"].replace("Z", "+00:00"))

    try:
        with Live(render_connection(ip, connected_time, expires_at), refresh_per_second=1, console=console) as live:
            while proc.poll() is None:
                live.update(render_connection(ip, connected_time, expires_at))
                time.sleep(1)
                if int(time.time() - connected_time) % 20 == 0:
                    connected = VPN.test_connection()
                    if connected and "ip" in connected:
                        ip = connected['ip']
                    else:
                        ip = "0.0.0.0"
    except KeyboardInterrupt:
        typer.echo("")
    
    # Always cleanup when exiting (whether by Ctrl+C or connection loss)
    with console.status("Disconnecting...", spinner="dots"):
        if proc.poll() is None:
            proc.send_signal(signal.SIGINT)
            proc.wait()
        OpenVPN.flush_routes()
        OpenVPN.reset_dns()

    typer.echo("Disconnected.")

@app.command()
def flush():
    """Flush routes and reset DNS."""
    OpenVPN.flush_routes()
    OpenVPN.reset_dns()
    typer.echo("Flushed routes and reset DNS.")

@app.command()
def reset():
    """Reset saved profiles and local network settings."""
    OpenVPN.flush_routes()
    OpenVPN.reset_dns()
    app_dir = os.path.expanduser("~/.grvpn")
    if os.path.exists(app_dir):
        for file in os.listdir(app_dir):
            os.remove(os.path.join(app_dir, file))
    typer.echo("Reset complete.")

def render_login(user):
    text = Text()
    text.append(f"Logged in as {user['email']}\n\n", style="bold magenta")
    text.append(f"ID: {user['id']}\n", style="")
    text.append(f"Name: {user['first_name']} {user['last_name']}\n", style="")
    text.append(f"Roles: {', '.join(user['roles'])}\n", style="")
    text.append(f"\nCreated at: {user['created_at']}", style="dim")
    return Panel(Align.left(text))

def render_connection(ip, connected_time, expires_at):
    elapsed = int(time.time() - connected_time)
    mins, secs = divmod(elapsed, 60)
    hrs, mins = divmod(mins, 60)
    timer_str = f"{hrs:02}:{mins:02}:{secs:02}"

    expires_in = int(expires_at.timestamp() - time.time())
    mins, secs = divmod(expires_in, 60)
    hrs, mins = divmod(mins, 60)
    expires_str = f"{hrs:02}:{mins:02}:{secs:02}"

    text = Text()
    if ip == "35.162.142.32":
        text.append("Connected to the Gaucho Racing VPN.\n\n", style="bold magenta")
        text.append(f"Public IP: {ip}\n", style="")
    else:
        text.append("Not connected to the Gaucho Racing VPN.\n\n", style="bold red")
        text.append(f"Public IP: {ip}\n", style="")
    text.append(f"Elapsed Time: {timer_str}\n", style="")
    text.append(f"Expires in: {expires_str}\n", style="")

    if ip == "35.162.142.32":
        text.append("\nPress Ctrl+C to disconnect", style="dim")
    else:
        text.append("\nPress Ctrl+C to exit", style="dim")

    return Panel(Align.left(text))

if __name__ == "__main__":
    app()