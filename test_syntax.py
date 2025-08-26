def run_model_plugin(prompt: str, selected: str, **kwargs) -> str:
    plugin_map = {"test": "value"}
    
    plugin = plugin_map.get(selected)
    if not plugin:
        return "Unknown plugin selection."
    try:
        msgs = prompt
        # If the plugin supports chat generation helpers, use them; else fall back to single-turn
        if hasattr(plugin, "generate_chat_via_providers"):
            # type: ignore[attr-defined]
            return "chat method"
        return "generate method"
    except Exception as e:
        # As a backup, attempt Ollama directly
        fallback = "ollama result"
        if fallback:
            return fallback
        return f"Model plugin error: {e}"

if __name__ == "__main__":
    print(run_model_plugin("test", "unknown"))
