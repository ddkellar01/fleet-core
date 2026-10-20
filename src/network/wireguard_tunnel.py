"""WireGuard tunnel manager — secure remote fleet control.

Renders wg0.conf, manages peers, brings the tunnel up/down. The fleet
API binds to the tunnel address so mission control is never exposed on
the public internet.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field


@dataclass
class Peer:
    name: str
    public_key: str
    allowed_ip: str           # e.g. 10.9.0.2/32
    endpoint: str = ""


@dataclass
class WireGuardTunnel:
    interface: str = "wg0"
    listen_port: int = 51821
    address: str = "10.9.0.1/24"
    private_key: str = ""     # from env WG_PRIVATE_KEY, never committed
    peers: list[Peer] = field(default_factory=list)

    def __post_init__(self):
        if not self.private_key:
            self.private_key = os.getenv("WG_PRIVATE_KEY", "")

    def add_peer(self, peer: Peer) -> None:
        self.peers = [p for p in self.peers if p.name != peer.name]
        self.peers.append(peer)

    def render_config(self) -> str:
        lines = ["[Interface]",
                 f"Address = {self.address}",
                 f"ListenPort = {self.listen_port}",
                 f"PrivateKey = {self.private_key or '<WG_PRIVATE_KEY>'}", ""]
        for p in self.peers:
            lines += ["[Peer]", f"# {p.name}",
                      f"PublicKey = {p.public_key}",
                      f"AllowedIPs = {p.allowed_ip}"]
            if p.endpoint:
                lines.append(f"Endpoint = {p.endpoint}")
            lines.append("")
        return "\n".join(lines)

    def write_config(self, path: str = "wg0.conf") -> str:
        with open(path, "w") as fh:
            fh.write(self.render_config())
        return path

    def _wg(self, *args: str) -> tuple[int, str]:
        try:
            out = subprocess.run(["wg-quick", *args],
                                 capture_output=True, text=True, timeout=15)
            return out.returncode, (out.stdout + out.stderr).strip()
        except FileNotFoundError:
            return 127, "wg-quick not installed (simulation mode)."
        except Exception as exc:  # pragma: no cover - host dependent
            return 1, str(exc)

    def up(self, config_path: str = "wg0.conf") -> tuple[int, str]:
        return self._wg("up", config_path)

    def down(self, config_path: str = "wg0.conf") -> tuple[int, str]:
        return self._wg("down", config_path)

    def status(self) -> dict:
        try:
            out = subprocess.run(["wg", "show", self.interface],
                                 capture_output=True, text=True, timeout=10)
            up = out.returncode == 0
            return {"interface": self.interface, "up": up,
                    "detail": out.stdout.strip() if up else "tunnel down"}
        except FileNotFoundError:
            return {"interface": self.interface, "up": False,
                    "detail": "wireguard tools not installed (simulation mode)"}