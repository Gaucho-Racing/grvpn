import shutil
import time
import signal
import subprocess
import sys
from grvpn.sudo_manager import SudoManager

class OpenVPN:

    @staticmethod
    def check_cli():
        return shutil.which("openvpn") is not None

    @staticmethod
    def connect(path: str, timeout: int = 30) -> subprocess.Popen | None:
        cmd = [
            "openvpn",
            "--config", path,
            "--dev", "tun_grvpn",
            "--connect-retry-max", "3",
            "--connect-timeout", "10",
            "--script-security", "2",
            "--route-delay", "1"
        ]
        try:
            proc = SudoManager.start_sudo_process(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
        except RuntimeError as e:
            print(f"Failed to start OpenVPN: {e}")
            return None

        start = time.time()
        try:
            for line in proc.stdout:
                if "Initialization Sequence Completed" in line:
                    return proc
                if time.time() - start > timeout:
                    proc.terminate()
                    return None
        except KeyboardInterrupt:
            proc.send_signal(signal.SIGINT)
            proc.wait()
            return None

        return None
    
    @staticmethod
    def flush_routes():
        try:
            SudoManager.run_sudo_shell_command("pkill openvpn")
            for i in range(10):
                SudoManager.run_sudo_shell_command(f"ifconfig utun{i} down", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            SudoManager.run_sudo_shell_command("route delete -net 0.0.0.0/1 10.8.0.1", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            SudoManager.run_sudo_shell_command("route delete -net 128.0.0.0/1 10.8.0.1", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except RuntimeError as e:
            print(f"Failed to flush routes: {e}")

    @staticmethod
    def set_dns():
        if sys.platform == "darwin":
            try:
                SudoManager.run_sudo_shell_command("networksetup -setdnsservers Wi-Fi 10.8.0.1")
            except RuntimeError as e:
                print(f"Failed to set DNS: {e}")
        elif sys.platform == "linux":
            pass
    
    @staticmethod
    def reset_dns():
        if sys.platform == "darwin":
            try:
                SudoManager.run_sudo_shell_command("networksetup -setdnsservers Wi-Fi empty")
            except RuntimeError as e:
                print(f"Failed to reset DNS: {e}")
        elif sys.platform == "linux":
            pass