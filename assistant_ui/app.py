"""CraftX Assistant - Streamlit Web Interface."""

# Standard library imports
import os
import sys
import logging
from datetime import datetime

# Third-party imports
import streamlit as st  # pylint: disable=import-error

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(
            os.path.dirname(__file__), 'craftx_assistant.log'))
    ]
)

# Set application metadata
APP_VERSION = "0.1.0"
APP_NAME = "CraftX.py Assistant"
APP_START_TIME = datetime.now().isoformat()
logging.info("Starting %s v%s at %s", APP_NAME, APP_VERSION, APP_START_TIME)

# Set path for local imports if necessary
# This ensures that import errors in the try block below provide useful info
sys_path_modified = False
if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'craftxpy')):
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        sys_path_modified = True
        logging.info("Added %s to sys.path", project_root)

try:
    from craftxpy.agents.router import AgentRouter
    from craftxpy.plugins.wizardcoder import WizardCoder
    from craftxpy.plugins.commandr7b import CommandR7B
    from craftxpy.plugins.codegeex4 import CodeGeeX4
    from craftxpy.plugins.qwen25coder import Qwen25Coder
    from craftxpy.memory.logger import ChatLogger
    from craftxpy.utils.shell import run_safe_command, get_safe_commands
    from craftxpy.plugins.tools import get_tools
    from craftxpy.utils.page_builder import build_craftx_page

    CRAFTX_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ CraftX.py modules not available: {e}")
    st.info("Make sure you're running from the correct directory and all dependencies are installed.")
    CRAFTX_AVAILABLE = False

# Configure Streamlit page
st.set_page_config(
    page_title="CraftX.py Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stop execution if CraftX.py modules aren't available
if not CRAFTX_AVAILABLE:
    st.stop()

# Custom CSS for CraftX.py branding
st.markdown("""
<style>
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1B1F3B, #2E2E2E);
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .main-header:hover {
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .logo-text {
        color: #00F0FF;
        font-size: 2rem;
        font-weight: bold;
        margin-left: 1rem;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    .tagline {
        color: #FFB300;
        font-style: italic;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stAlert > div {
        background-color: rgba(0, 240, 255, 0.1);
        border: 1px solid #00F0FF;
        border-radius: 8px;
    }
    /* Improved chat message styling */
    .user-message {
        background-color: rgba(0, 240, 255, 0.05);
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 3px solid #00F0FF;
        margin-bottom: 1rem;
    }
    .assistant-message {
        background-color: rgba(255, 179, 0, 0.05);
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 3px solid #FFB300;
        margin-bottom: 1rem;
    }
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="logo-text">🧠 CraftX.py Assistant <span style="font-size: 0.6em; vertical-align: super; opacity: 0.8;">v{APP_VERSION}</span></div>
</div>
<div class="tagline">Python-native intelligence, modular by design.</div>
""", unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = "default"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")

# Model Selection
st.sidebar.subheader("🤖 AI Model")
model_classes = {
    "WizardCoder": WizardCoder,
    "CommandR7B": CommandR7B,
    "CodeGeeX4": CodeGeeX4,
    "Qwen2.5-Coder": Qwen25Coder
}
selected_model = st.sidebar.selectbox(
    "Choose Model:",
    options=list(model_classes.keys()),
    index=0
)

# Lazy instantiation of the selected model
if "model_instance" not in st.session_state or st.session_state.get("model_name") != selected_model:
    st.session_state.model_instance = model_classes[selected_model]()
    st.session_state.model_name = selected_model

# Initialize router with selected model instance
router = AgentRouter(models={"active": st.session_state.model_instance})

# Chat Logger
logger = ChatLogger()

# Session Management
st.sidebar.subheader("💬 Session")
sessions = logger.list_sessions()
if sessions:
    session_choice = st.sidebar.selectbox(
        "Load Session:", ["New Session"] + sessions)
    if session_choice != "New Session":
        st.session_state.session_id = session_choice
        st.session_state.chat_history = logger.load(session_choice)

# Development Mode
st.sidebar.subheader("🛠️ Developer Tools")
dev_mode = st.sidebar.checkbox("Enable Dev Mode", value=False)
show_model_info = st.sidebar.checkbox("Show Model Info", value=False)

if show_model_info:
    st.sidebar.json(router.list_models())

# File Upload Section
st.sidebar.subheader("📁 File Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload a file", type=["py", "txt", "md", "json", "csv"])
if uploaded_file:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        with st.sidebar.expander("File Content", expanded=False):
            st.code(file_content, language="python" if uploaded_file.name.endswith(
                ".py") else "text")
    except UnicodeDecodeError:
        st.sidebar.error(
            "❌ Could not decode file as UTF-8. Please upload a UTF-8 encoded file.")

# Main Chat Interface
st.subheader("💬 Chat Interface")

# Display chat history
chat_container = st.container()
with chat_container:
    for entry in st.session_state.chat_history:
        role = entry.get("role", "user")
        message = entry.get("message", "")
        timestamp = entry.get("timestamp", "")

        # Format timestamp for better readability
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%b %d, %Y • %I:%M %p")
        except (ValueError, TypeError):
            formatted_time = timestamp

        if role == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>🧑 You</strong> <em style="font-size: 0.8em; opacity: 0.8;">{formatted_time}</em>
                <div style="margin-top: 0.5rem;">{message}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🤖 CraftX.py</strong> <em style="font-size: 0.8em; opacity: 0.8;">{formatted_time}</em>
                <div style="margin-top: 0.5rem;">{message}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

prompt = st.text_input("Type your message:",
                       value=st.session_state.prompt, key="chat_input")

if prompt:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "message": prompt,
        "timestamp": datetime.now().isoformat()
    })
    logger.save(st.session_state.session_id, prompt, "user")

    # Generate response
    with st.spinner("🤖 Thinking..."):
        # Check if it's a special command
        if prompt.startswith("/"):
            command = prompt[1:].strip()
            if command in get_safe_commands():
                response = run_safe_command(command)
            else:
                response = f"❌ Command not recognized. Available commands: {', '.join(get_safe_commands())}"
        else:
            # Use AI model with error handling
            try:
                response = router.route("active", prompt)
            except (ValueError, TypeError, AttributeError) as e:
                response = f"❌ Model configuration error: {str(e)}"
                logging.error("Model configuration error", exc_info=True)
            except (ConnectionError, TimeoutError) as e:
                response = f"❌ Network error while accessing model: {str(e)}"
                logging.error("Network error with model", exc_info=True)
            except (RuntimeError, KeyError) as e:
                response = f"❌ Model runtime error: {str(e)}"
                logging.error("Model runtime error", exc_info=True)

    st.session_state.chat_history.append({
        "role": "assistant",
        "message": response,
        "timestamp": datetime.now().isoformat()
    })
    logger.save(st.session_state.session_id, response, "assistant")

    # Clear prompt and rerun to update display
    st.session_state.prompt = ""
    st.rerun()

# Tools Section
st.subheader("🔧 Available Tools")

# Load tools
tools = get_tools()

if tools:
    tool_tabs = st.tabs(list(tools.keys()))
    for i, (tool_name, tool_instance) in enumerate(tools.items()):
        with tool_tabs[i]:
            tool_info = tool_instance.get_tool_info()
            st.markdown(f"""
            <div style="padding: 1rem; background-color: rgba(0, 240, 255, 0.05); border-radius: 8px; margin-bottom: 1rem; border-left: 3px solid #00F0FF;">
                <strong>{tool_info['description']}</strong>
                <div style="font-size: 0.8em; margin-top: 0.5rem; opacity: 0.8;">
                    Version: {tool_info.get('version', '1.0.0')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            tool_params = {}
            try:
                # Create expandable section for parameters
                with st.expander("Tool Parameters", expanded=True):
                    for param_name, param_info in tool_info.get('parameters', {}).items():
                        param_type = param_info.get('type')
                        param_desc = param_info.get('description', '')
                        required = param_info.get('required', False)

                        # Add visual indicator for required parameters
                        label = f"{param_name.title()}{'*' if required else ''}:"

                        if param_type == 'string':
                            tool_params[param_name] = st.text_input(
                                label,
                                key=f"{tool_name}_{param_name}",
                                help=param_desc
                            )
                        elif param_type == 'integer':
                            tool_params[param_name] = st.number_input(
                                label,
                                key=f"{tool_name}_{param_name}",
                                value=param_info.get('default', 0),
                                help=param_desc
                            )
                        elif param_type == 'boolean':
                            tool_params[param_name] = st.checkbox(
                                label,
                                key=f"{tool_name}_{param_name}",
                                help=param_desc
                            )
                        elif param_type == 'float':
                            tool_params[param_name] = st.number_input(
                                label,
                                key=f"{tool_name}_{param_name}",
                                value=param_info.get('default', 0.0),
                                help=param_desc,
                                format="%.4f"
                            )

                # Add validation for required parameters
                missing_params = [p for p, v in tool_params.items()
                                  if tool_info.get('parameters', {}).get(p, {}).get('required', False)
                                  and (v is None or v == '')]

                if missing_params:
                    st.warning(
                        f"Required parameters missing: {', '.join(missing_params)}")
                    run_disabled = True
                else:
                    run_disabled = False

                # Run button with loading state
                if st.button(f"Run {tool_name}", key=f"run_{tool_name}", disabled=run_disabled):
                    with st.spinner(f"Running {tool_name}..."):
                        try:
                            # Log tool execution
                            logging.info(
                                "Executing tool: %s with params: %s", tool_name, tool_params)
                            start_time = datetime.now()

                            result = tool_instance.run(**tool_params)

                            # Calculate execution time
                            execution_time = (
                                datetime.now() - start_time).total_seconds()
                            st.success(
                                f"Tool executed successfully in {execution_time:.2f} seconds")

                            # Display result in a collapsible section if it's lengthy
                            if len(result) > 500:
                                with st.expander("View Result", expanded=True):
                                    st.code(result)
                            else:
                                st.code(result)

                            # Add option to copy result to clipboard via JavaScript
                            # Fix for f-string with backslash issue
                            escaped_result = result.replace('`', r'\`')
                            st.markdown(
                                f"""
                                <button onclick="navigator.clipboard.writeText(`{escaped_result}`)">
                                    📋 Copy to Clipboard
                                </button>
                                """,
                                unsafe_allow_html=True
                            )
                        except ValueError as e:
                            st.error(f"Invalid parameter value: {str(e)}")
                            logging.warning(
                                "Tool execution failed with ValueError: %s", str(e))
                        except (AttributeError, TypeError) as e:
                            st.error(f"Tool execution failed: {str(e)}")
                            logging.error(
                                "Tool execution failed with %s: %s", type(e).__name__, str(e))
                        except ModuleNotFoundError as e:
                            st.error(f"Tool dependency missing: {str(e)}")
                            st.info(
                                "Try installing the required package with pip.")
                            logging.error(
                                "Tool dependency missing: %s", str(e))
                        except ImportError as e:
                            st.error(f"Import error: {str(e)}")
                            logging.error("Import error in tool: %s", str(e))
                        except OSError as e:
                            st.error(f"System error: {str(e)}")
                            logging.error(
                                "OS error in tool execution: %s", str(e))
                        except (RuntimeError, KeyError, IndexError) as e:
                            st.error(f"Runtime error: {str(e)}")
                            if dev_mode:  # Show full traceback only in dev mode
                                st.exception(e)
                            logging.error(
                                "Runtime error in tool execution: %s", str(e), exc_info=True)
            except ValueError as e:
                st.error(f"Tool configuration error: {str(e)}")
                if dev_mode:
                    st.exception(e)
                logging.error("Tool configuration error: %s",
                              str(e), exc_info=True)
else:
    st.info("No tools available. Check the tools directory.")

# Developer Mode Section
if dev_mode:
    st.subheader("🛠️ Developer Mode")

    col1, col2 = st.columns(2)

    with col1:
        shell_cmd = st.text_input("Command:")
        if shell_cmd:
            if st.button("Execute"):
                trimmed_cmd = shell_cmd.strip()
                result = run_safe_command(trimmed_cmd)
                st.code(result)

    with col2:
        st.subheader("Page Builder")
        page_title = st.text_input("Page Title:", value="CraftX.py Page")
        page_content = st.text_area(
            "Page Content:", value="<p>Hello from CraftX.py!</p>")
        page_filename = st.text_input("Filename:", value="craftx_demo.html")

        if st.button("Build Page"):
            result = build_craftx_page(page_title, page_content, page_filename)
            st.success(result)

# Calculate app uptime


def get_uptime():
    start = datetime.fromisoformat(APP_START_TIME)
    now = datetime.now()
    delta = now - start
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{delta.days}d {hours}h {minutes}m {seconds}s"


# Footer with status
st.markdown("<hr style='border: 1px solid #222; margin-top: 2rem; margin-bottom: 1rem;' />",
            unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #222; font-size: 0.9rem; background-color: #F9F9F9; padding: 0.5rem 0; border-radius: 6px;'>
    <p>CraftX.py v{APP_VERSION} - Python-native intelligence, modular by design.</p>
    <p>
        🔗 <a href="https://craftx.dev" target="_blank" rel="noopener noreferrer" style="color:#005A9E; text-decoration:underline;">Visit the CraftX Developer Portal</a> |
        🔗 <a href="https://craftxpy.com" target="_blank" rel="noopener noreferrer" style="color:#005A9E; text-decoration:underline;">Learn more at CraftXPy.com</a> |
        🔗 <a href="https://craftx.ai" target="_blank" rel="noopener noreferrer" style="color:#005A9E; text-decoration:underline;">Explore CraftX AI Solutions</a>
    </p>
    <p style='font-size: 0.8rem; opacity: 0.7;'>
        ⏱️ Uptime: {get_uptime()} | 🛠️ System: {sys.platform} | 📊 Sessions: {len(sessions) if sessions else 0}
    </p>
</div>
""", unsafe_allow_html=True)
