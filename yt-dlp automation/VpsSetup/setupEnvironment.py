#!/usr/bin/env python3

import subprocess
import sys
import os

commands = [
    {
        "name": "Install Python3",
        "cmd": ["apt", "install", "-y", "python3"]
    },
    {
        "name": "Install pip",
        "cmd": ["apt", "install", "-y", "python3-pip"]
    },
    {
        "name": "Upgrade pip",
        "cmd": ["python3", "-m", "pip", "install", "--upgrade", "pip"]
    },
    {
        "name": "Install yt-dlp",
        "cmd": ["pip", "install", "yt-dlp"]
    },
    {
        "name": "APT update",
        "cmd": ["apt-get", "update"]
    },
    {
        "name": "Install ffmpeg",
        "cmd": ["apt-get", "install", "-y", "ffmpeg"]
    },
    {
        "name": "System upgrade",
        "cmd": ["apt", "upgrade", "-y"]
    },
    {
        "name": "Install OpenSSH",
        "cmd": ["apt", "install", "-y", "openssh-server", "openssh-client"]
    },
    {
        "name": "Add sshuser",
        "cmd": ["adduser", "sshuser"]
    },
    {
        "name": "Add sshuser to sudo group",
        "cmd": ["usermod", "-aG", "sudo", "sshuser"]
    },
    {
        "name": "Install Tailscale (script)",
        "cmd": ["bash", "-c", "curl -fsSL https://tailscale.com/install.sh | sh"]
    },
    {
        "name": "Install Tailscale keyring",
        "cmd": [
            "bash", "-c",
            "curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg "
            "| tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null"
        ]
    },
    {
        "name": "Install Tailscale repo",
        "cmd": [
            "bash", "-c",
            "curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list "
            "| tee /etc/apt/sources.list.d/tailscale.list"
        ]
    },
    {
        "name": "APT update (Tailscale)",
        "cmd": ["apt", "update"]
    },
    {
        "name": "Install Tailscale",
        "cmd": ["apt", "install", "-y", "tailscale"]
    },
    {
        "name": "Start tailscaled",
        "cmd": ["tailscaled", "--tun=userspace-networking &"]
    }
]


def run_command(step):
    print(f"\n▶ Menjalankan: {step['name']}")
    result = subprocess.run(step["cmd"])

    if result.returncode != 0:
        while True:
            choice = input(
                f"❌ Error pada perintah '{step['name']}'. "
                "Lanjutkan ke perintah berikutnya? (Y/N): "
            ).strip().lower()

            if choice == "y":
                return True
            elif choice == "n":
                print("⛔ Script dihentikan oleh user.")
                sys.exit(1)
            else:
                print("Masukkan Y atau N saja.")


def main():
    if os.geteuid() != 0:
        print("❌ Script ini harus dijalankan dengan sudo.")
        sys.exit(1)

    for step in commands:
        run_command(step)

    print("\n✅ Semua perintah selesai dijalankan.")

if __name__ == "__main__":
    main()
