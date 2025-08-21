"""
CraftX.py Custom Analytics Dashboard (Simple Version)
Privacy-focused analytics without external dependencies
"""

import streamlit as st
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="CraftX.py Analytics",
    page_icon="📊",
    layout="wide"
)


def get_analytics_data():
    """Get analytics data from SQLite database"""
    db_path = Path("craftx_analytics.db")

    if not db_path.exists():
        return []

    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT event_id, timestamp, event_type, user_id, session_id, properties, source, version
                FROM analytics_events 
                ORDER BY timestamp DESC 
                LIMIT 100
            """)

            results = cursor.fetchall()

            events = []
            for row in results:
                try:
                    properties = json.loads(row[5]) if row[5] else {}
                except json.JSONDecodeError:
                    properties = {}

                events.append({
                    "event_id": row[0],
                    "timestamp": row[1],
                    "event_type": row[2],
                    "user_id": row[3],
                    "session_id": row[4],
                    "properties": properties,
                    "source": row[6],
                    "version": row[7]
                })

            return events

    except Exception as e:
        st.error(f"Error loading analytics data: {e}")
        return []


def count_events_by_type(events):
    """Count events by type"""
    counts = {}
    for event in events:
        event_type = event['event_type']
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts


def main():
    """Main dashboard function"""

    # Header
    st.title("🔒 CraftX.py Custom Analytics")
    st.markdown("### Privacy-focused analytics with complete local control")

    # Privacy information
    with st.expander("🔒 Privacy Information", expanded=False):
        st.markdown("""
        **✅ What we collect (locally):**
        - Application usage events (start/stop)
        - OAuth authentication attempts (success/failure)
        - Plugin usage statistics
        - Error occurrences for debugging
        
        **❌ What we DON'T collect:**
        - Personal information
        - File contents or code
        - Network traffic
        - External API calls
        
        **🏠 Data storage:**
        - Everything stored locally in SQLite
        - No data sent to external servers
        - You control your data completely
        """)

    # Load analytics data
    events = get_analytics_data()

    if not events:
        st.info(
            "📊 No analytics data found yet. Data will appear here as you use CraftX.py features.")

        st.markdown("""
        ### 🚀 Getting Started
        
        Your analytics system is configured and ready! Analytics will be collected when you:
        
        - **Use OAuth authentication** - Login attempts tracked
        - **Run plugins** - Usage statistics recorded  
        - **Use WebAuthn** - Passkey authentication tracked
        - **Application events** - Start/stop events logged
        
        All data stays on your machine and is never transmitted externally.
        """)
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Events", len(events))

    with col2:
        unique_sessions = len(set(event['session_id'] for event in events))
        st.metric("Unique Sessions", unique_sessions)

    with col3:
        event_types = len(set(event['event_type'] for event in events))
        st.metric("Event Types", event_types)

    with col4:
        if events:
            latest_event = max(events, key=lambda x: x['timestamp'])
            latest_time = datetime.fromisoformat(
                latest_event['timestamp'].replace('Z', '+00:00'))
            time_diff = datetime.now(timezone.utc) - latest_time

            if time_diff.days > 0:
                last_activity = f"{time_diff.days} days ago"
            elif time_diff.seconds > 3600:
                last_activity = f"{time_diff.seconds // 3600} hours ago"
            else:
                last_activity = f"{time_diff.seconds // 60} minutes ago"

            st.metric("Last Activity", last_activity)

    # Event distribution
    st.subheader("📈 Event Distribution")

    event_counts = count_events_by_type(events)

    # Simple bar chart using Streamlit's built-in chart
    if event_counts:
        chart_data = []
        for event_type, count in event_counts.items():
            chart_data.extend([event_type] * count)

        # Display as a simple table
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Event Type Counts:**")
            for event_type, count in sorted(event_counts.items()):
                st.write(f"• **{event_type}**: {count}")

        with col2:
            # Use Streamlit's bar chart
            import pandas as pd
            df = pd.DataFrame(list(event_counts.items()),
                              columns=['Event Type', 'Count'])
            st.bar_chart(df.set_index('Event Type'))

    # Recent events
    st.subheader("🕒 Recent Events")

    if events:
        # Show recent events in a table
        recent_events = events[:20]  # Show last 20 events

        table_data = []
        for event in recent_events:
            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(
                    event['timestamp'].replace('Z', '+00:00'))
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = event['timestamp']

            # Format properties
            props_str = ""
            if event['properties']:
                key_props = []
                for key, value in event['properties'].items():
                    if key not in ['timestamp', 'session_id']:
                        key_props.append(f"{key}: {value}")
                props_str = ", ".join(key_props[:3])  # Show first 3 properties

            table_data.append({
                "Time": formatted_time,
                "Type": event['event_type'],
                "Source": event['source'] or 'system',
                "Properties": props_str
            })

        # Display as Streamlit dataframe
        import pandas as pd
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

    # Data export
    st.subheader("💾 Data Export")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Export All Data"):
            # Create export data
            export_data = {
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "total_events": len(events),
                "events": events
            }

            # Convert to JSON
            json_data = json.dumps(export_data, indent=2)

            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"craftx_analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    with col2:
        if st.button("🗑️ Clear All Data"):
            st.warning("⚠️ This will permanently delete all analytics data!")
            if st.button("Confirm Delete", type="primary"):
                try:
                    db_path = Path("craftx_analytics.db")
                    if db_path.exists():
                        with sqlite3.connect(str(db_path)) as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM analytics_events")
                            conn.commit()
                        st.success("✅ All analytics data deleted!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error deleting data: {e}")


if __name__ == "__main__":
    main()
