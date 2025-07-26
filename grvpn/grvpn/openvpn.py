import shutil
import time
import signal
import subprocess
import sys

class OpenVPN:

    @staticmethod
    def check_cli():
        return shutil.which("openvpn") is not None

    @staticmethod
    def connect(path: str, timeout: int = 30) -> subprocess.Popen | None:
        cmd = [
            "sudo", "openvpn",
            "--config", path,
            "--dev", "tun_grvpn",
            "--connect-retry-max", "3",
            "--connect-timeout", "10",
            "--script-security", "2",
            "--route-delay", "1"
        ]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

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
        subprocess.run("sudo pkill openvpn", shell=True)
        for i in range(10):
            subprocess.run(f"sudo ifconfig utun{i} down", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("sudo route delete -net 0.0.0.0/1 10.8.0.1", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("sudo route delete -net 128.0.0.0/1 10.8.0.1", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def set_dns():
        if sys.platform == "darwin":
            subprocess.run("sudo networksetup -setdnsservers Wi-Fi 10.8.0.1", shell=True)
        elif sys.platform == "linux":
            pass
    
    @staticmethod
    def reset_dns():
        if sys.platform == "darwin":
            subprocess.run("sudo networksetup -setdnsservers Wi-Fi empty", shell=True)
        elif sys.platform == "linux":
            pass