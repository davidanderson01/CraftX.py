"""DNS validation tool for CraftX.py."""

import dns.exception
import dns.resolver

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
            ,
 "record_type": {
 "type": "string",
 "description": "Type of DNS record to retrieve (A, AAAA, MX, TXT, etc.). Defaults to A.",
 "required": False,
 "default": "A"
 }
        }

    def run(self, domain: str = None, record_type: str = "A", **kwargs) -> str:
        """Validate DNS resolution for a domain.

        Args:
            domain: The domain name to validate
 record_type: The type of DNS record to retrieve (e.g., "A", "AAAA", "MX", "TXT").
 Defaults to "A".
            **kwargs: Additional parameters (ignored)

        Returns:
            DNS validation result
        """
        if not domain:
 return "❌ Domain parameter is required."

        if not domain.strip():
 return "❌ Domain cannot be empty."

        try:
 resolver = dns.resolver.Resolver()
 resolver.timeout = 5
 resolver.lifetime = 5
 answers = resolver.resolve(domain.strip(), record_type.strip().upper())
 result = f"✅ {record_type.strip().upper()} records for {domain}:\n"
 for rdata in answers:
 result += f"- {rdata}\n"
 return result
        except dns.resolver.NoAnswer:
 return f"❌ No {record_type.strip().upper()} records found for {domain}."
        except dns.exception.DNSException as e:
 return f"❌ DNS query failed for {domain} ({record_type.strip().upper()}): {str(e)}"
