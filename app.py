"""
MoveInSync Play Store Intelligence Dashboard & Recurring Monitoring System
Designed for Product Managers, Engineering Leads, and Leadership to monitor
real-time commuter sentiment, detect version regressions, and track Jira action items.
"""

import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="MoveInSync - Play Store Intelligence Monitor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 18px;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .ticket-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        border-left: 5px solid #e53935;
    }
    .ticket-card-p1 {
        border-left-color: #fb8c00;
    }
    .ticket-card-p2 {
        border-left-color: #1e88e5;
    }
    .user-quote {
        background-color: #f1f3f4;
        border-radius: 6px;
        padding: 10px 14px;
        font-style: italic;
        color: #37474f;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not os.path.exists("data/analyzed_reviews.csv") or not os.path.exists("data/app_metadata.json"):
        st.error("Data files not found. Please run `python src/scraper.py` and `python src/analyzer.py` first.")
        return None, None
        
    with open("data/app_metadata.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    df = pd.read_csv("data/analyzed_reviews.csv")
    return meta, df

meta, df = load_data()

if df is not None:
    # Sidebar Controls
    st.sidebar.image("https://moveinsync.com/wp-content/uploads/2021/04/moveinsync-logo.png", width=180)
    st.sidebar.title("Commuter Pulse")
    st.sidebar.caption("Continuous Google Play Store Review Intelligence")
    
    st.sidebar.divider()
    st.sidebar.subheader("Filters")
    
    selected_ratings = st.sidebar.multiselect(
        "Filter by Star Rating",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5]
    )
    
    categories = ["All"] + sorted(list(df["category"].dropna().unique()))
    selected_category = st.sidebar.selectbox("Category", categories)
    
    stages = ["All"] + sorted(list(df["journey_stage"].dropna().unique()))
    selected_stage = st.sidebar.selectbox("Journey Stage", stages)
    
    teams = ["All"] + sorted(list(df["team"].dropna().unique()))
    selected_team = st.sidebar.selectbox("Responsible Team", teams)
    
    search_keyword = st.sidebar.text_input("Search Review Content", "")

    # Apply Filters
    filtered_df = df[df["rating"].isin(selected_ratings)]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    if selected_stage != "All":
        filtered_df = filtered_df[filtered_df["journey_stage"] == selected_stage]
    if selected_team != "All":
        filtered_df = filtered_df[filtered_df["team"] == selected_team]
    if search_keyword:
        filtered_df = filtered_df[filtered_df["content"].str.contains(search_keyword, case=False, na=False)]

    # Main Dashboard Header
    st.title("🚗 MoveInSync: Play Store Rating Intelligence Platform")
    st.caption("Addressing: *'Why are our Play Store ratings where they are, and what do we do first?'*")

    # High-level Metrics Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Store Rating", f"{meta.get('score', 4.32)} ★", f"{meta.get('ratings_count', 114880):,} total")
    with c2:
        st.metric("Analyzed Dataset", f"{len(df)} reviews", f"{len(filtered_df)} filtered")
    with c3:
        neg_pct = round((df["rating"] <= 2).sum() / len(df) * 100, 1)
        st.metric("Negative Sentiment", f"{neg_pct}%", "1★ & 2★ reviews")
    with c4:
        p0_count = (df["severity"] == "P0_CRITICAL").sum()
        st.metric("P0 Critical Blockers", f"{p0_count}", "Trip failure / Safety")
    with c5:
        app_version = meta.get("current_version", "Latest")
        st.metric("Target App Package", "ETS Employee", f"v{app_version}")

    st.markdown("---")

    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Pulse & Sentiment Analytics",
        "🗺️ Journey Stage Breakdown",
        "🚀 Release Version Regressions",
        "📋 Next-Day Engineering Backlog",
        "💡 Rating Intercept Strategy"
    ])

    with tab1:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Rating Distribution")
            rating_counts = filtered_df["rating"].value_counts().sort_index().reset_index()
            rating_counts.columns = ["Rating", "Count"]
            colors = ["#e53935", "#fb8c00", "#fdd835", "#7cb342", "#2e7d32"]
            fig_rating = px.bar(
                rating_counts,
                x="Rating",
                y="Count",
                text="Count",
                color="Rating",
                color_discrete_sequence=colors,
                title="Star Rating Breakdown"
            )
            fig_rating.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1), showlegend=False)
            st.plotly_chart(fig_rating, use_container_width=True)

        with col_right:
            st.subheader("Functional Category Breakdown")
            cat_counts = filtered_df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig_cat = px.pie(
                cat_counts,
                values="Count",
                names="Category",
                hole=0.45,
                title="Negative vs Positive Issue Distribution"
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        st.subheader("High-Impact Public Pain Points (Ranked by Community Upvotes & Rating Drag)")
        top_drag = filtered_df.sort_values(by="drag_score", ascending=False).head(5)
        for _, row in top_drag.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="ticket-card {'ticket-card-p1' if row['severity']=='P1_HIGH' else 'ticket-card-p2'}">
                    <strong>{row['rating']}★ | {row['category']} | Severity: {row['severity']} | Upvotes: 👍 {row['thumbs_up']} | Version: {row['app_version']}</strong>
                    <div class="user-quote" style="margin-top:8px;">"{row['content']}"</div>
                    <div style="margin-top:6px; font-size:13px; color:#555;">
                        <b>Root Cause Hypothesis:</b> {row['root_cause_summary']} &nbsp;|&nbsp; <b>Actionable Owner:</b> {row['team']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Commuter Friction Along the 7 Journey Touchpoints")
        st.write("Mapping complaints against the operational flow described in MoveInSync's problem brief:")

        stage_df = filtered_df[filtered_df["journey_stage"] != "Overall_Experience"]
        stage_counts = stage_df["journey_stage"].value_counts().reset_index()
        stage_counts.columns = ["Journey Stage", "Count"]
        
        fig_stage = px.bar(
            stage_counts,
            x="Count",
            y="Journey Stage",
            orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale="Reds",
            title="Complaints by Commute Touchpoint"
        )
        fig_stage.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_stage, use_container_width=True)

        st.info("""
        **Key Findings:**
        1. **Live Tracking & ETA (82 issues):** Commuters experience extreme anxiety when cab markers freeze or jump across roads.
        2. **Ride Booking & Waitlist (79 issues):** Confusion between confirmed seats vs waitlisted rosters during shift booking.
        3. **Roster & Authentication (50 issues):** Frequent logouts and app crashes on launch locking employees out of office commutes.
        4. **Boarding & OTP Verification (18 issues):** Direct trip blocker—missing OTPs or popups preventing quick driver verification.
        """)

    with tab3:
        st.subheader("Release Version Regression Tracking")
        st.write("Tracking which app releases caused rating drops and crash spikes:")
        
        v_df = df[df["app_version"] != "Unknown"].groupby("app_version").agg(
            total_reviews=("rating", "count"),
            avg_rating=("rating", "mean"),
            negative_count=("rating", lambda x: (x <= 2).sum())
        ).reset_index()
        v_df = v_df[v_df["total_reviews"] >= 6].sort_values(by="avg_rating")

        fig_v = px.bar(
            v_df,
            x="app_version",
            y="avg_rating",
            color="avg_rating",
            color_continuous_scale="RdYlGn",
            text=v_df["avg_rating"].round(2),
            title="Average Rating by App Release Version (min. 6 reviews)"
        )
        fig_v.add_hline(y=4.0, line_dash="dash", line_color="green", annotation_text="Target Rating Threshold (4.0★)")
        st.plotly_chart(fig_v, use_container_width=True)

        st.warning("""
        **Release Regression Audit:**
        - **v11.4.13 (1.14★):** Severe regression where map automatically zoomed out every 3 seconds.
        - **v12.11.2 (1.96★) & v12.16.1 (1.92★):** Critical database migration crash and repetitive logout bugs after updating.
        - **v12.19.0 (3.62★):** Introduction of blocking seatbelt popup over the 'View OTP' button, causing boarding delays.
        """)

    with tab4:
        st.subheader("Jira-Ready Engineering Backlog (Start Tomorrow)")
        st.write("Specific, prioritized engineering specifications addressing the root causes:")

        from src.prioritization import generate_prioritized_tickets
        tickets = generate_prioritized_tickets(df)

        for t in tickets:
            p_class = "ticket-card" if "P0" in t["priority"] else ("ticket-card ticket-card-p1" if "P1" in t["priority"] else "ticket-card ticket-card-p2")
            with st.container():
                st.markdown(f"""
                <div class="{p_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="margin:0; color:#1a237e;">[{t['ticket_id']}] {t['title']}</h4>
                        <span style="font-weight:bold; color:#d32f2f;">{t['priority']}</span>
                    </div>
                    <p style="margin: 4px 0 10px 0; color:#555;"><b>Target Team:</b> {t['team']} &nbsp;|&nbsp; <b>Impact:</b> {t['impact_metrics']}</p>
                    <div class="user-quote">"{t['user_voice']}"</div>
                    <div style="margin-top:10px;">
                        <b>Technical Root Cause:</b><br>{t['root_cause']}
                    </div>
                    <div style="margin-top:8px;">
                        <b>Engineering Specification:</b><br><pre style="white-space:pre-wrap; font-family:inherit; background:#fafafa; padding:8px; border-radius:4px;">{t['solution']}</pre>
                    </div>
                    <div style="margin-top:8px;">
                        <b>Acceptance Criteria:</b><br><pre style="white-space:pre-wrap; font-family:inherit; background:#f1f8e9; padding:8px; border-radius:4px;">{t['acceptance_criteria']}</pre>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab5:
        st.subheader("Play Store Reputation & Rating Intercept Strategy")
        st.write("How to mathematically move Play Store rating from **4.32★ to 4.70★** without changing a line of backend fleet routing:")

        from src.prioritization import generate_rating_growth_strategy
        strat = generate_rating_growth_strategy()

        st.markdown(f"""
        ### 1. The Core Problem
        {strat['problem_diagnosis']}

        ### 2. The 3 Strategic Pillars
        """)

        for p in strat['solution_pillars']:
            st.markdown(f"""
            #### {p['pillar']}
            {p['details']}
            """)

        st.success(f"""
        ### Projected Rating Lift
        {strat['projected_impact']}
        """)

    # Footer note
    st.markdown("---")
    st.caption("MoveInSync FDE Intelligence Pipeline | Automated Google Play Store Review Analytics")
