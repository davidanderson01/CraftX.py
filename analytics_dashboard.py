"""
Custom Analytics Dashboard for CraftX.py
Privacy-focused analytics visualization without external dependencies
"""

import streamlit as st
import json
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from craftxpy.utils.custom_analytics import CustomAnalytics, AnalyticsConfig
except ImportError:
    st.error("Could not import CustomAnalytics. Make sure the module is available.")
    st.stop()


def main():
    st.set_page_config(
        page_title="CraftX.py Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 CraftX.py Custom Analytics Dashboard")
    st.markdown("*Privacy-focused analytics with local data storage*")

    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Analytics Controls")

        # Privacy information
        if st.button("🔒 Show Privacy Info"):
            st.info("""
            **Privacy-First Analytics**
            
            ✅ All data stored locally
            ❌ No external tracking
            ✅ You control your data
            ❌ No Microsoft/Azure telemetry
            """)

        # Analytics controls
        st.subheader("Data Management")

        if st.button("📥 Export Data"):
            analytics = CustomAnalytics()
            data = analytics.export_data()
            st.download_button(
                label="Download JSON",
                data=data,
                file_name=f"craftx_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.button("⚠️ Confirm Delete", type="secondary"):
                analytics = CustomAnalytics()
                analytics.clear_data(confirm=True)
                st.success("Data cleared!")
                st.rerun()

        # Time range selector
        st.subheader("📅 Time Range")
        days = st.selectbox("Show data for last:", [
                            1, 7, 30, 90, 365], index=1)

    # Main dashboard
    analytics = CustomAnalytics()

    # Check if analytics is enabled
    if not analytics.enable_collection:
        st.warning(
            "📊 Analytics collection is disabled. Enable it to see insights.")
        if st.button("Enable Analytics"):
            AnalyticsConfig.enable_minimal_analytics()
            st.rerun()
        return

    # Get analytics summary
    summary = analytics.get_analytics_summary(days=days)

    if "error" in summary:
        st.error(f"Error loading analytics: {summary['error']}")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📈 Total Events",
            value=summary.get("total_events", 0)
        )

    with col2:
        st.metric(
            label="🔄 Active Sessions",
            value=summary.get("unique_sessions", 0)
        )

    with col3:
        st.metric(
            label="📅 Time Period",
            value=f"{days} days"
        )

    with col4:
        st.metric(
            label="🎯 Event Types",
            value=len(summary.get("event_breakdown", {}))
        )

    # Event breakdown chart
    if summary.get("event_breakdown"):
        st.subheader("📊 Event Distribution")

        event_data = summary["event_breakdown"]
        df = pd.DataFrame(list(event_data.items()),
                          columns=["Event Type", "Count"])

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = px.pie(
                df,
                values="Count",
                names="Event Type",
                title="Event Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(
                df.sort_values("Count", ascending=False),
                x="Event Type",
                y="Count",
                title="Events by Type"
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)

    # Recent events table
    st.subheader("📋 Recent Events")

    try:
        with sqlite3.connect(analytics.db_path) as conn:
            query = """
                SELECT timestamp, event_type, properties 
                FROM analytics_events 
                WHERE timestamp > datetime('now', '-{} days')
                ORDER BY timestamp DESC 
                LIMIT 50
            """.format(days)

            df_events = pd.read_sql_query(query, conn)

            if not df_events.empty:
                # Parse properties for display
                df_events["properties_parsed"] = df_events["properties"].apply(
                    lambda x: json.loads(x) if x else {}
                )

                # Create a cleaner display
                display_df = df_events[["timestamp", "event_type"]].copy()
                display_df["timestamp"] = pd.to_datetime(
                    display_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")

                st.dataframe(display_df, use_container_width=True)

                # Show detailed view for selected event
                if st.checkbox("Show event details"):
                    selected_idx = st.selectbox(
                        "Select event:", range(len(df_events)))
                    if selected_idx is not None:
                        event = df_events.iloc[selected_idx]
                        st.json(event["properties_parsed"])
            else:
                st.info("No events found for the selected time period.")

    except Exception as e:
        st.error(f"Error loading events: {e}")

    # Usage insights
    st.subheader("💡 Usage Insights")

    insights = []
    event_counts = summary.get("event_breakdown", {})

    if "oauth_authentication" in event_counts:
        insights.append(
            f"🔐 OAuth authentication used {event_counts['oauth_authentication']} times")

    if "plugin_activity" in event_counts:
        insights.append(
            f"🧩 Plugins used {event_counts['plugin_activity']} times")

    if "ai_model_usage" in event_counts:
        insights.append(
            f"🤖 AI models used {event_counts['ai_model_usage']} times")

    if "error_occurred" in event_counts:
        insights.append(f"⚠️ {event_counts['error_occurred']} errors occurred")

    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("Start using CraftX.py to see usage insights here!")

    # Footer
    st.markdown("---")
    st.markdown("""
    **🔒 Privacy Notice**: This dashboard shows data stored locally on your machine. 
    No data is sent to external servers or third parties.
    """)


if __name__ == "__main__":
    main()
