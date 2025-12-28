"""Port scanning service."""

from typing import List, Dict, Any
import socket


class PortScanner:
    """Port scanning service."""

    @staticmethod
    def scan_port(host: str, port: int, timeout: int = 3) -> Dict[str, Any]:
        """Scan a single port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                return {
                    "port": port,
                    "status": "open",
                    "service": PortScanner._get_service_name(port),
                }
            else:
                return {
                    "port": port,
                    "status": "closed",
                    "service": PortScanner._get_service_name(port),
                }
        except socket.gaierror:
            return {"port": port, "status": "error", "error": "Hostname could not be resolved"}
        except socket.error:
            return {"port": port, "status": "filtered", "error": "Connection refused"}

    @staticmethod
    def _get_service_name(port: int) -> str:
        """Get service name for port."""
        services = {
            20: "FTP-DATA",
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            5432: "PostgreSQL",
            27017: "MongoDB",
        }
        return services.get(port, "Unknown")
