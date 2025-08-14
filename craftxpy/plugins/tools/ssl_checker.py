"""SSL certificate checker tool for CraftX.py."""

import socket
import ssl
from datetime import datetime

from .base_tool import BaseTool


class SSLCertChecker(BaseTool):
    """Tool for checking SSL certificate information."""

    def __init__(self):
        super().__init__()
        self.description = "Check SSL certificate information for domains"
        self.version = "1.0.0"
        self.parameters = {
            "domain": {
                "type": "string",
                "description": "Domain name to check SSL certificate",
                "required": True
            },
            "port": {
                "type": "integer",
                "description": "Port number (default: 443)",
                "required": False,
                "default": 443
            }
        }

    def run(self, domain: str = None, port: int = 443, **kwargs) -> str:
        """Check SSL certificate for a domain.

        Args:
            domain: The domain name to check
            port: The port number (default: 443)
            **kwargs: Additional parameters (ignored)

        Returns:
            SSL certificate check result
        """
        if not domain:
            return "❌ Domain parameter is required"

        if not domain.strip():
            return "❌ Domain cannot be empty"

        try:
            # Create SSL context
            context = ssl.create_default_context()

            # Connect and get certificate
            with socket.create_connection((domain.strip(), port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain.strip()) as ssock:
                    cert = ssock.getpeercert()

            # Parse certificate information
            if not cert:
                return f"❌ No certificate found for {domain}:{port}"

            # Extract expiration date
            expiry_str = cert.get('notAfter')
            if expiry_str:
                expiry_date = datetime.strptime(
                    expiry_str, "%b %d %H:%M:%S %Y %Z")
                days_until_expiry = (expiry_date - datetime.now()).days

                if days_until_expiry < 0:
                    status = f"❌ EXPIRED {abs(days_until_expiry)} days ago"
                elif days_until_expiry < 30:
                    status = f"⚠️ Expires in {days_until_expiry} days"
                else:
                    status = f"✅ Expires in {days_until_expiry} days"

                expiry_info = f"{status} ({expiry_date.strftime('%Y-%m-%d')})"
            else:
                expiry_info = "❓ Expiration date not found"

            # Extract issuer information
            issuer_dict = dict(x[0] for x in cert.get('issuer', []))
            issuer = issuer_dict.get('organizationName', 'Unknown')

            return f"✅ SSL Certificate for {domain}:{port}\n" \
                f"   Issuer: {issuer}\n" \
                f"   Status: {expiry_info}"

        except socket.timeout:
            return f"❌ Connection timeout for {domain}:{port}"
        except socket.gaierror:
            return f"❌ DNS resolution failed for {domain}"
        except ssl.SSLError as e:
            return f"❌ SSL error for {domain}:{port}: {str(e)}"
        except (OSError, ConnectionError) as e:
            return f"❌ Connection error checking {domain}:{port}: {str(e)}"
