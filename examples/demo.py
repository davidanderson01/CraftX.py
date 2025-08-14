"""CraftX.py Demo - Basic usage examples."""

import os
import sys

# Add parent directory to path so we can import craftxpy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from craftxpy.agents.router import AgentRouter
    from craftxpy.memory.logger import ChatLogger
    from craftxpy.plugins.codegeex4 import CodeGeeX4
    from craftxpy.plugins.commandr7b import CommandR7B
    from craftxpy.plugins.qwen25coder import Qwen25Coder
    from craftxpy.plugins.tools import get_tools
    from craftxpy.plugins.wizardcoder import WizardCoder
    from craftxpy.utils.shell import run_safe_command

    CRAFTX_AVAILABLE = True
except ImportError as e:
    print(f"❌ CraftX.py modules not available: {e}")
    print("Make sure you're running from the correct directory.")
    CRAFTX_AVAILABLE = False


def main():
    """Demonstrate basic CraftX.py functionality."""
    if not CRAFTX_AVAILABLE:
        return

    print("🧠 CraftX.py Demo - Python-native intelligence, modular by design.")
    print("=" * 60)

    # 1. Model Router Demo
    print("\n1. 🤖 AI Model Router Demo")
    print("-" * 30)

    # Initialize models
    models = {
        "codegen": WizardCoder(),
        "reasoning": CommandR7B(),
        "multilang": CodeGeeX4(),
        "advanced": Qwen25Coder()
    }

    router = AgentRouter(models=models)

    # Test different models
    prompts = [
        ("codegen", "Write a PowerShell script to check disk space"),
        ("reasoning", "Explain the benefits of modular AI architecture"),
        ("multilang",
         "Convert this Python function to JavaScript: def hello(name): return f'Hello {name}'"),
        ("advanced", "Create a FastAPI endpoint for user authentication")
    ]

    for task_type, prompt in prompts:
        print(f"\n📝 Task: {task_type}")
        print(f"Prompt: {prompt}")
        response = router.route(task_type, prompt)
        print(f"Response: {response}")

    # 2. Memory Logger Demo
    print("\n\n2. 💾 Memory Logger Demo")
    print("-" * 30)

    logger = ChatLogger()
    session_id = "demo_session"

    # Save some demo conversations
    demo_messages = [
        ("user", "Hello CraftX.py!"),
        ("assistant", "Hello! I'm CraftX.py, your modular AI assistant."),
        ("user", "Can you help me with Python code?"),
        ("assistant", "Absolutely! I can help with code generation, debugging, and explanations.")
    ]

    for role, message in demo_messages:
        logger.save(session_id, message, role)

    # Load and display conversation
    conversation = logger.load(session_id)
    print(f"\n📜 Conversation history for session '{session_id}':")
    for entry in conversation:
        role_emoji = "🧑" if entry["role"] == "user" else "🤖"
        print(f"{role_emoji} [{entry['timestamp']}] {entry['message']}")

    # 3. Safe Shell Demo
    print("\n\n3. 🛡️ Safe Shell Demo")
    print("-" * 30)

    safe_commands = ["whoami", "hostname", "echo Hello CraftX.py"]

    for cmd in safe_commands:
        print(f"\n$ {cmd}")
        result = run_safe_command(cmd)
        print(result)

    # Test unsafe command
    print("\n$ rm -rf /")
    result = run_safe_command("rm -rf /")
    print(result)

    # 4. Tools Demo
    print("\n\n4. 🔧 Tools Demo")
    print("-" * 30)

    tools = get_tools()
    print(f"Available tools: {list(tools.keys())}")

    # Test DNS Validator if available
    if "DNSValidator" in tools:
        print("\n🌐 Testing DNS Validator:")
        dns_tool = tools["DNSValidator"]
        test_domains = ["google.com", "github.com",
                        "nonexistent-domain-12345.com"]

        for domain in test_domains:
            result = dns_tool.run(domain=domain)
            print(f"  {result}")

    # Test SSL Checker if available
    if "SSLCertChecker" in tools:
        print("\n🔒 Testing SSL Certificate Checker:")
        ssl_tool = tools["SSLCertChecker"]
        test_sites = ["google.com", "github.com"]

        for site in test_sites:
            result = ssl_tool.run(domain=site)
            print(f"  {result}")

    print("\n" + "=" * 60)
    print("✅ CraftX.py demo completed successfully!")
    print("🚀 Ready to build amazing AI-powered applications!")


if __name__ == "__main__":
    main()
