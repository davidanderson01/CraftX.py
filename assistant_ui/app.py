"""
CraftX.py Assistant - Streamlit Web Interface
A modern, interactive UI for CraftX.py intelligence framework.
"""

import json
import os
import sys
import tempfile
from datetime import datetime

import streamlit as st

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Configure Streamlit page
st.set_page_config(
    page_title="CraftX.py Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f3e5f5;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def load_chat_history():
    """Load chat history from file."""
    chat_logs_dir = os.path.join(project_root, 'chat_logs')
    default_log = os.path.join(chat_logs_dir, 'default.json')

    if os.path.exists(default_log):
        try:
            with open(default_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


def save_chat_history(history):
    """Save chat history to file."""
    chat_logs_dir = os.path.join(project_root, 'chat_logs')
    os.makedirs(chat_logs_dir, exist_ok=True)
    default_log = os.path.join(chat_logs_dir, 'default.json')

    with open(default_log, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)


def main():
    """Main application function."""
    # Header with logo
    logo_path = os.path.join(project_root, 'assets', 'img', 'craftx-logo.png')
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_path, width=400)

    st.markdown("""
    <div class="main-header">
        <h1>🧠 CraftX.py Assistant</h1>
        <p>Python-native intelligence, modular by design</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🛠️ Settings")

        # Model selection
        model_options = [
            "WizardCoder",
            "CommandR7B",
            "CodeGeeX4",
            "Qwen2.5-Coder"
        ]
        selected_model = st.selectbox("🤖 Select AI Model", model_options)

        # Session management
        st.subheader("📝 Session")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            save_chat_history([])
            st.rerun()

        # Tools
        st.subheader("🔧 Tools")
        tools_enabled = st.checkbox("Enable Tools", value=True)

        # System info
        st.subheader("ℹ️ System Info")
        st.text(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
        st.text(f"Streamlit: {st.__version__}")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    # Display chat history
    st.subheader("💬 Conversation")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Handle both "content" and "message" keys for compatibility
                content = message.get("content") or message.get("message", "")
                st.markdown(content)

    # Chat input
    if prompt := st.chat_input("Ask CraftX.py anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # For now, provide a placeholder response
                # In a real implementation, this would route to the AI models
                response = f"""
                🤖 **{selected_model} Response:**
                
                I received your message: "{prompt}"
                
                This is a demo response from the CraftX.py assistant. In a full implementation, 
                this would be processed by the selected AI model ({selected_model}) with 
                access to the following capabilities:
                
                - 🔧 Tool integration: {"Enabled" if tools_enabled else "Disabled"}
                - 🧠 Multi-model routing
                - 💾 Persistent memory
                - 🛡️ Secure execution
                
                Current timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                """

                st.markdown(response)

        # Add assistant response to history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

        # Save chat history
        save_chat_history(st.session_state.messages)

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🔗 Links:**")
        st.markdown("- [GitHub](https://github.com/davidanderson01/craftxpy)")
        st.markdown("- [Documentation](https://docs.craftx.py)")

    with col2:
        st.markdown("**📊 Stats:**")
        st.markdown(f"- Messages: {len(st.session_state.messages)}")
        st.markdown(f"- Model: {selected_model}")

    with col3:
        st.markdown("**⚡ Quick Actions:**")
        if st.button("📚 Show Examples"):
            st.info("Check the examples/ directory for code samples!")
        if st.button("🧪 Run Tests"):
            st.info("Use 'python run.py' option 3 to run tests!")


if __name__ == "__main__":
    main()
