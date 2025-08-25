import os
import subprocess
import getpass
from typing import Optional

class SudoManager:
    """Manages sudo password storage and execution for improved UX."""
    
    # Static class variable for password file location
    _password_file = os.path.expanduser("~/.grvpn/sudo.txt")
    
    @staticmethod
    def _ensure_grvpn_dir():
        """Create ~/.grvpn directory with secure permissions if it doesn't exist."""
        grvpn_dir = os.path.expanduser("~/.grvpn")
        if not os.path.exists(grvpn_dir):
            os.makedirs(grvpn_dir)
    
    @staticmethod
    def _save_password(password: str):
        """Save password to file with secure permissions."""
        SudoManager._ensure_grvpn_dir()
        with open(SudoManager._password_file, 'w') as f:
            f.write(password)
    
    @staticmethod
    def _load_password() -> Optional[str]:
        """Load password from file."""
        if not os.path.exists(SudoManager._password_file):
            return None
        try:
            with open(SudoManager._password_file, 'r') as f:
                return f.read().strip()
        except (IOError, OSError):
            return None
    
    @staticmethod
    def _validate_password(password: str) -> bool:
        """Validate sudo password by running a simple command."""
        try:
            result = subprocess.run(
                ["sudo", "-S", "-k", "true"],
                input=f"{password}\n",
                text=True,
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            return False
    
    @staticmethod
    def _prompt_password() -> str:
        """Prompt user for sudo password."""
        return getpass.getpass("Enter sudo password: ")
    
    @staticmethod
    def ensure_sudo_access() -> bool:
        """Ensure we have a valid sudo password, prompting if necessary."""
        # Try to load existing password
        password = SudoManager._load_password()
        
        # Validate existing password
        if password and SudoManager._validate_password(password):
            return True
        
        # Clear any cached sudo credentials
        subprocess.run(["sudo", "-k"], capture_output=True)
        
        # Prompt for new password and validate
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                password = SudoManager._prompt_password()
                if SudoManager._validate_password(password):
                    SudoManager._save_password(password)
                    return True
                else:
                    print(f"Invalid password. {max_attempts - attempt - 1} attempts remaining.")
            except KeyboardInterrupt:
                print("\nSudo authentication cancelled.")
                return False
            except Exception as e:
                print(f"Error during sudo authentication: {e}")
                return False
        
        print("Failed to authenticate after maximum attempts.")
        return False
    
    @staticmethod
    def run_sudo_command(command: list, **kwargs) -> subprocess.CompletedProcess:
        """Run a sudo command using stored password."""
        if not SudoManager.ensure_sudo_access():
            raise RuntimeError("Failed to obtain sudo access")
        
        password = SudoManager._load_password()
        if not password:
            raise RuntimeError("No valid sudo password available")
        
        # Add sudo and -S flag to command
        sudo_command = ["sudo", "-S"] + command
        
        # Set default kwargs for subprocess
        default_kwargs = {
            "input": f"{password}\n",
            "text": True
        }
        
        # Only set capture_output if stdout/stderr aren't explicitly provided
        if 'stdout' not in kwargs and 'stderr' not in kwargs:
            default_kwargs["capture_output"] = True
        
        default_kwargs.update(kwargs)
        
        return subprocess.run(sudo_command, **default_kwargs)
    
    @staticmethod
    def run_sudo_shell_command(command: str, **kwargs) -> subprocess.CompletedProcess:
        """Run a sudo shell command using stored password."""
        if not SudoManager.ensure_sudo_access():
            raise RuntimeError("Failed to obtain sudo access")
        
        password = SudoManager._load_password()
        if not password:
            raise RuntimeError("No valid sudo password available")
        
        # Prepare shell command with sudo
        sudo_command = f"echo '{password}' | sudo -S {command}"
        
        # Set default kwargs for subprocess
        default_kwargs = {
            "shell": True,
            "text": True
        }
        
        # Only set capture_output if stdout/stderr aren't explicitly provided
        if 'stdout' not in kwargs and 'stderr' not in kwargs:
            default_kwargs["capture_output"] = True
        
        default_kwargs.update(kwargs)
        
        return subprocess.run(sudo_command, **default_kwargs)
    
    @staticmethod
    def start_sudo_process(command: list, **kwargs) -> subprocess.Popen:
        """Start a sudo process (like OpenVPN) using stored password."""
        if not SudoManager.ensure_sudo_access():
            raise RuntimeError("Failed to obtain sudo access")
        
        password = SudoManager._load_password()
        if not password:
            raise RuntimeError("No valid sudo password available")
        
        # Add sudo and -S flag to command
        sudo_command = ["sudo", "-S"] + command
        
        # Set default kwargs for subprocess
        default_kwargs = {
            "stdin": subprocess.PIPE,
            "text": True
        }
        default_kwargs.update(kwargs)
        
        # Start the process
        proc = subprocess.Popen(sudo_command, **default_kwargs)
        
        # Send password to stdin
        if proc.stdin:
            proc.stdin.write(f"{password}\n")
            proc.stdin.flush()
        
        return proc
