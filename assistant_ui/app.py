"""
CraftX.py Assistant UI

A Streamlit-based user interface for the CraftX.py AI framework.
Provides an interactive chat interface for users to interact with the AI assistants.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# For capability discovery
import importlib
import pathlib
import sys
try:
    import craftxpy  # type: ignore
except ModuleNotFoundError:
    # Add repo root to sys.path so local package resolves when running from source
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
    try:
        import craftxpy  # type: ignore
    except ModuleNotFoundError:
        craftxpy = None  # fallback; discovery will scan filesystem

# Set page configuration
st.set_page_config(
    page_title="CraftX.py Assistant",
    page_icon="[AI]",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main function for the CraftX.py Assistant UI."""
    st.title("[AI] CraftX.py Assistant")
    st.markdown("**Python-native intelligence, modular by design.**")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        st.info("Configure your AI assistant settings here.")

        # Plugin selection
        st.subheader("Available Plugins")
        plugins = [
            "Ollama (local)",
            "CraftX (custom)",
            "CodeGeeX4",
            "CommandR7B",
            "Qwen2.5-Coder",
            "WizardCoder",
        ]
        selected_plugin = st.selectbox("Select AI Plugin:", plugins)
        st.caption(
            "Tip: For provider-backed models, run Ollama locally or set OPENAI_API_KEY.")

        # Chat settings
        st.subheader("Chat Settings")
        max_tokens = st.slider("Max Tokens:", 100, 4000, 1000)
        temperature = st.slider("Temperature:", 0.0, 2.0, 0.7, step=0.01)

        # Persona/style
        style = st.selectbox(
            "Reply Style:",
            ["Concise (default)", "ElevateCraft (ethics + creativity)",
             "Technical (code-first)"],
        )

        # Capabilities
        st.subheader("Capabilities")
        caps = discover_capabilities()
        with st.expander(f"Agents ({len(caps['agents'])})", expanded=False):
            if caps["agents"]:
                for a in caps["agents"]:
                    st.markdown(f"- {a}")
            else:
                st.caption("No agents detected")
        with st.expander(f"Models/Plugins ({len(caps['models'])})", expanded=False):
            if caps["models"]:
                for m in caps["models"]:
                    st.markdown(f"- {m}")
            else:
                st.caption("No model plugins detected")
        with st.expander(f"Tools ({len(caps['tools'])})", expanded=False):
            if caps["tools"]:
                for t in caps["tools"]:
                    st.markdown(f"- {t}")
            else:
                st.caption("No tools detected")
        with st.expander(f"Utilities ({len(caps['utilities'])})", expanded=False):
            if caps["utilities"]:
                for u in caps["utilities"]:
                    st.markdown(f"- {u}")
            else:
                st.caption("No utilities detected")

    # Main chat interface
    st.header("Chat Interface")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(
        "Type your message or tool command...",
        help="Examples: 'dns A github.com', 'ssl craftx.elevatecraft.org', or chat (select Ollama)"
    ):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response (tool dispatcher first, else plugin)
        with st.chat_message("assistant"):
            response = handle_prompt(prompt)
            if not response:
                response = run_model_plugin(
                    prompt,
                    selected_plugin,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    style=style,
                )
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

    # Footer
    st.markdown("---")
    st.markdown("*Powered by CraftX.py • ElevateCraft*")


# -------- Helpers moved to helpers.py --------
from .helpers import (
    discover_capabilities,
    titleize,
    handle_prompt,
    parse_dns_intent,
    parse_ssl_intent,
    run_ollama,
    _build_system_prompt,
    _build_messages_from_history,
)


def run_model_plugin(prompt: str, selected: str, **kwargs) -> str:
    """Dispatch to the selected model plugin with provider-backed generation.

    Falls back to Ollama direct or a helpful message if providers are unavailable.
    """
    try:
        from craftxpy.plugins import CodeGeeX4, CommandR7B, Qwen25Coder, WizardCoder, CraftXModel  # type: ignore
    except Exception:
        # As a last resort, try local Ollama
        return run_ollama(prompt) or "No model providers available. Install/run Ollama or set OPENAI_API_KEY."

    plugin_map = {}
    try:
        from craftxpy.plugins import CodeGeeX4, CommandR7B, Qwen25Coder, WizardCoder, CraftXModel  # type: ignore
        plugin_map = {
            "CodeGeeX4": CodeGeeX4(),
            "CommandR7B": CommandR7B(),
            "Qwen2.5-Coder": Qwen25Coder(),
            "WizardCoder": WizardCoder(),
            "CraftX (custom)": CraftXModel(),
        }
    except Exception:
        # Plugins not available, will handle gracefully below
        pass
    style = kwargs.get("style", "Concise (default)")
    if selected == "Ollama (local)":
        msgs = _build_messages_from_history(prompt, style=style)
        # Try chat style via Ollama first (if available), else fall back to single-turn
        try:
            import ollama  # type: ignore
            model = os.environ.get("CRAFTX_OLLAMA_MODEL", "llama3.1")
            res = ollama.chat(model=model, messages=msgs)
            content = res.get("message", {}).get("content")
            if content:
                return content
        except Exception:
            pass
        return run_ollama(prompt) or "Ollama not available. Install/run Ollama or choose another plugin."

    plugin = plugin_map.get(selected)
    if not plugin:
        return f"Unknown plugin selection: '{selected}'."
    msgs = _build_messages_from_history(prompt, style=style)
    try:
        # If the plugin supports chat generation helpers, use them; else fall back to single-turn
        if hasattr(plugin, "generate_chat_via_providers"):
            # type: ignore[attr-defined]
            return plugin.generate_chat_via_providers(msgs, **kwargs)
        return plugin.generate(prompt, **kwargs)
    except Exception as e:
        # As a backup, attempt Ollama directly
        fallback = run_ollama(prompt)
        if fallback:
            return fallback
        return f"Model plugin error: {e}"


if __name__ == "__main__":
    main()
