"""DNS validation tool for CraftX.py."""

import socket
from .base_tool import BaseTool


class DNSValidator(BaseTool):
    """Tool for validating DNS resolution of domain names."""

    def __init__(self):
        super().__init__()
        self.description = "Validate DNS resolution for domain names"
        self.version = "1.0.0"
        self.parameters = {
            "domain": {
                "type": "string",
                "description": "Domain name to validate",
                "required": True
            }
        }

    def run(self, domain: str = None, **kwargs) -> str:
        """Validate DNS resolution for a domain.

        Args:
            domain: The domain name to validate
            **kwargs: Additional parameters (ignored)

        Returns:
            DNS validation result
        """
        if not domain:
            return "❌ Domain parameter is required"

        if not domain.strip():
            return "❌ Domain cannot be empty"

        try:
            # Resolve domain to IP address
            ip_address = socket.gethostbyname(domain.strip())
            return f"✅ {domain} → {ip_address}"
        except socket.gaierror as e:
            return f"❌ DNS resolution failed for {domain}: {str(e)}"
        except (OSError, UnicodeError) as e:
            return f"❌ Network error validating {domain}: {str(e)}"
