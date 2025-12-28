"""SSL/TLS certificate validation service."""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import ssl
import socket


class SSLValidator:
    """SSL/TLS certificate validation."""

    @staticmethod
    def validate_domain(domain: str) -> Dict[str, Any]:
        """Validate SSL certificate for domain."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cert_bin = ssock.getpeercert(binary_form=True)

                    # Parse certificate details
                    subject = dict(x[0] for x in cert["subject"])
                    issuer = dict(x[0] for x in cert["issuer"])

                    # Check expiration
                    not_after_str = cert["notAfter"]
                    not_after = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                    days_until_expiry = (not_after - datetime.now()).days

                    status = "valid"
                    if days_until_expiry < 0:
                        status = "expired"
                    elif days_until_expiry < 30:
                        status = "expiring"

                    return {
                        "domain": domain,
                        "status": status,
                        "issuer": issuer.get("organizationName", "Unknown"),
                        "subject": subject.get("commonName", domain),
                        "valid_from": cert["notBefore"],
                        "valid_until": cert["notAfter"],
                        "days_until_expiry": days_until_expiry,
                        "san": cert.get("subjectAltName", []),
                    }
        except Exception as e:
            return {
                "domain": domain,
                "status": "error",
                "error": str(e),
            }
